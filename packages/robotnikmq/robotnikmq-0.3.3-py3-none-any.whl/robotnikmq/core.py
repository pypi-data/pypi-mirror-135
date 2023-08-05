from contextlib import contextmanager
from datetime import datetime
from json import loads as from_json
from json.decoder import JSONDecodeError
from pathlib import Path
from random import sample
from ssl import SSLError
from threading import current_thread
from typing import Optional, Callable, Any, Dict, Union, Generator, List
from uuid import uuid4 as uuid, UUID

from arrow import Arrow, get as to_arrow, now
from funcy import first
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPError, AMQPConnectionError
from pydantic import BaseModel  # pylint: disable=E0611
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig, conn_params_of, config_of
from robotnikmq.error import UnableToConnect, MalformedMessage
from robotnikmq.utils import to_json

AMQPErrorCallback = Optional[Callable[[AMQPError], None]]
ConnErrorCallback = Optional[Callable[[AMQPConnectionError], None]]


@contextmanager
def thread_name(name: Union[str, UUID]):
    thread = current_thread()
    original = thread.name
    thread.name = str(name)
    yield
    thread.name = original


@typechecked
def jsonable(content: Any) -> bool:
    try:
        to_json(content)
        return True
    except (TypeError, OverflowError):
        return False


@typechecked
def valid_json(string: str) -> bool:
    try:
        from_json(string)
        return True
    except JSONDecodeError:
        return False


class Message:
    @typechecked
    def __init__(self, contents: Union[BaseModel, Dict[str, Any]],
                 routing_key: Optional[str] = None,
                 timestamp: Union[int, float, datetime, None] = None,
                 msg_id: Union[str, UUID, None] = None):
        self.msg_id = msg_id or uuid()
        if not jsonable(contents):
            raise ValueError("Contents of message have to be JSON-serializeable")
        self.contents = contents.dict() if isinstance(contents, BaseModel) else contents
        self.routing_key: str = routing_key or ''
        self.timestamp: Arrow = to_arrow(timestamp) if timestamp is not None else now()

    @typechecked
    def to_dict(self) -> Dict[str, Any]:
        return {'routing_key': self.routing_key,
                'contents': self.contents,
                'msg_id': str(self.msg_id),
                'timestamp': self.timestamp.int_timestamp}

    @typechecked
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @staticmethod
    @typechecked
    def of(body: str) -> 'Message':  # pylint: disable=C0103
        try:
            msg = from_json(body)
            return Message(msg['contents'], msg['routing_key'], msg['timestamp'], msg['msg_id'])
        except (JSONDecodeError, KeyError) as exc:
            raise MalformedMessage(body) from exc

    @typechecked
    def __getitem__(self, key: str) -> Any:
        return self.contents[key]

    def keys(self):
        return self.contents.keys()

    def values(self):
        return self.contents.values()

    @typechecked
    def __contains__(self, item: str) -> bool:
        return item in self.contents

    def __iter__(self):
        return iter(self.contents)

    @property
    def route(self) -> str:
        return self.routing_key


class Robotnik:
    @typechecked
    def __init__(self, config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None,
                 config_paths: Optional[List[Path]] = None):
        config_paths = config_paths or [Path.cwd() / 'robotnikmq.yaml',
                                        Path.home() / '.config' / 'robotnikmq' / 'robotnikmq.yaml',
                                        Path('/etc/robotnikmq/robotnikmq.yaml')]
        self.config = config or config_of(first(path for path in config_paths if path.exists()))
        self._connection = None
        self._channel: Optional[BlockingChannel] = None
        self._on_conn_error = on_conn_error

    @typechecked
    def _make_connection(self) -> BlockingConnection:
        errors: Dict[str, str] = {}
        for tier in self.config.tiers:
            for config in sample(tier, len(tier)):
                try:
                    return BlockingConnection(conn_params_of(config))
                except (AMQPConnectionError, SSLError) as exc:
                    errors[f'{config.user}@{config.host}:{config.port}'] = str(exc)
                    if self._on_conn_error is not None:
                        self._on_conn_error(exc)
        raise UnableToConnect(f'Cannot connect to any of the configured servers: {errors}')

    @property
    def connection(self) -> BlockingConnection:
        if self._connection is None or not self._connection.is_open:
            self._connection = self._make_connection()
        return self._connection

    @typechecked
    def _open_channel(self) -> BlockingChannel:
        _channel = self.connection.channel()
        _channel.basic_qos(prefetch_count=1)
        return _channel

    @property
    def channel(self) -> BlockingChannel:
        if self._channel is None or not self._channel.is_open:
            self._channel = self._open_channel()
        return self._channel

    @contextmanager
    def open_channel(self) -> Generator[BlockingChannel, None, None]:
        _ch = self.channel
        yield _ch
        self.close_channel(_ch)

    @typechecked
    def close_channel(self, channel: Optional[BlockingChannel] = None) -> None:
        channel = channel or self.channel
        if channel is not None and channel.is_open:
            channel.stop_consuming()
            channel.close()
