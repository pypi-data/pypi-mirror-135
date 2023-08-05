from time import time
from typing import Optional, Any, Dict, Union, List
from uuid import uuid4 as uuid

from pika import BasicProperties
from typeguard import typechecked

from robotnikmq.core import Robotnik, RobotnikConfig, ConnErrorCallback
from robotnikmq.rpc_server import RpcError, RpcResponse
from robotnikmq.utils import to_json


class RpcClient(Robotnik):
    @typechecked
    def __init__(self, config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None):
        super().__init__(config=config, on_conn_error=on_conn_error)
        self.response: Optional[Any] = None
        self.callback_queue = None
        self.corr_id = str(uuid())

    @typechecked
    def _on_response(self, _, __, props: BasicProperties, body: bytes) -> None:
        self.response = body.decode() if self.corr_id == props.correlation_id else None

    @typechecked
    def call(self, queue: str,
             args: Optional[Dict[str, Any]] = None,
             str_args: Optional[str] = None,
             timeout: Optional[float] = None,
             raise_on_error: bool = False) -> Union[RpcError, str, int, float,
                                                    Dict[str, Any], List[Dict[str, Any]]]:
        with self.open_channel() as channel:
            result = channel.queue_declare(queue='', exclusive=True)
            self.callback_queue = result.method.queue
            channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self._on_response,
                auto_ack=True)
            self.response = None
            self.corr_id = str(uuid())
            str_args = str_args or '{}'
            channel.basic_publish(exchange='',
                                  routing_key=queue,
                                  properties=BasicProperties(reply_to=self.callback_queue,
                                                             correlation_id=self.corr_id),
                                  body=to_json(args) if args is not None else str_args)
            start_time = time()
            while self.response is None:
                self.connection.process_data_events()
                if timeout is not None and time() > start_time + timeout:
                    raise TimeoutError(f'No response has been received for Request: {self.corr_id}')
            response = RpcResponse.from_json(self.response)
            if response is not None:
                return response.data
            error = RpcError.from_json(self.response)
            if raise_on_error:
                raise RuntimeError(error.details)
            return error
