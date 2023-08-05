from inspect import signature, Parameter
from json import loads as from_json
from traceback import format_exc
from socket import gethostname
from typing import Optional, Callable, Union, Any, Dict, Tuple, List
from typing import get_type_hints, get_origin, get_args
from uuid import uuid4 as uuid, UUID

from pika import BasicProperties
from pika.exceptions import AMQPError, ChannelError, AMQPConnectionError
from retry import retry
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, ConnErrorCallback, thread_name, valid_json
from robotnikmq.log import log
from robotnikmq.utils import to_json


@typechecked
def _type_hint_str(typ: Any) -> str:
    if get_origin(typ) is Union:
        return f"Union[{','.join([_type_hint_str(t) for t in get_args(typ)])}]"
    return str(typ.__name__)


class RpcError():
    @typechecked
    def __init__(self, request_id: Union[str, UUID, None] = None,
                 details: Union[None, str, Dict[str, Any]] = None):
        self.request_id = request_id or uuid()
        self.details = details

    @typechecked
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @typechecked
    def to_dict(self) -> Dict[str, Any]:
        return {'request_id': str(self.request_id),
                'type': 'error',
                'details': self.details}

    @staticmethod
    @typechecked
    def from_json(json_str: Union[str, bytes]) -> Optional['RpcError']:
        json_str = json_str if isinstance(json_str, str) else json_str.decode()
        log.debug(json_str)
        if valid_json(json_str):
            data = from_json(json_str)
            if all(k in data for k in {'request_id', 'type', 'details'}):
                return RpcError(request_id=data['request_id'],
                                details=data['details'])
        return None


class RpcResponse():
    @typechecked
    def __init__(self,
                 request_id: Union[str, UUID, None] = None,
                 data: Union[None, str, int, float, Dict[str, Any],
                             List[Dict[str, Any]]] = None):
        self.request_id = request_id or uuid()
        self.data = data

    @typechecked
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @typechecked
    def to_dict(self) -> Dict[str, Any]:
        return {'request_id': str(self.request_id),
                'type': 'response',
                'data': self.data}

    @staticmethod
    @typechecked
    def from_json(json_str: Union[str, bytes]) -> Optional['RpcResponse']:
        json_str = json_str if isinstance(json_str, str) else json_str.decode()
        if valid_json(json_str):
            data = from_json(json_str)
            if all(k in data for k in {'request_id', 'type', 'data'}):
                return RpcResponse(request_id=data['request_id'],
                                   data=data['data'])
        return None


class RpcServer(Robotnik):
    @typechecked
    def __init__(self, config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None,
                 meta_queue_prefix: Optional[str] = None,
                 docs_queue_suffix: Optional[str] = None,
                 only_once: bool = False):
        super().__init__(config=config, on_conn_error=on_conn_error)
        self._callbacks: Dict[str, Callable] = {}
        self.meta_queue_prefix = meta_queue_prefix or gethostname()
        self.docs_queue_suffix = docs_queue_suffix or '.__doc__'
        # Typically used for testing, implies server should stop after 1 response
        self.only_once = only_once

    @typechecked
    def _register_docs(self, queue: str, callback: Callable) -> None:
        self.channel.queue_declare(queue=queue + self.docs_queue_suffix, exclusive=False)

        @typechecked
        def docs_callback(_, method, props: BasicProperties, __) -> None:
            req_id = props.correlation_id or uuid()
            response = RpcResponse(req_id,
                                   data={'rpc_queue': queue,
                                         'inputs': self._get_input_type_strings(queue),
                                         'returns': self._get_return_type_str(queue),
                                         'description': callback.__doc__})
            self.channel.basic_publish(exchange='',
                                       routing_key=props.reply_to,
                                       properties=BasicProperties(
                                        correlation_id=props.correlation_id),
                                       body=response.to_json())
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue + self.docs_queue_suffix,
                                   on_message_callback=docs_callback,
                                   auto_ack=False)

    @typechecked
    def _get_defaults(self, queue: str) -> Dict[str, Any]:
        params = signature(self._callbacks[queue]).parameters
        return {p: params[p].default for p in params if params[p].default is not Parameter.empty}

    @typechecked
    def _get_input_types(self, queue: str) -> Dict[str, Any]:
        return {k: v for k, v in get_type_hints(self._callbacks[queue]).items() if k != 'return'}

    @typechecked
    def _get_input_type_strings(self, queue: str) -> Dict[str, Any]:
        return {k: _type_hint_str(v) for k, v in
                get_type_hints(self._callbacks[queue]).items() if k != 'return'}

    @typechecked
    def _get_return_type_str(self, queue: str) -> Any:
        return _type_hint_str(get_type_hints(self._callbacks[queue])['return'])

    @staticmethod
    @typechecked
    def _is_optional(arg_type: Any) -> bool:
        return get_origin(arg_type) is Union and type(None) in get_args(arg_type)

    @staticmethod
    @typechecked
    def _valid_arg(arg_value: Any, arg_type: Any) -> bool:
        if arg_type is Any:
            return True
        if get_origin(arg_type) is Union:
            if (type(None) in get_args(arg_type)) and (arg_value is None or arg_value == {}):  # Optional
                return True
            return any(RpcServer._valid_arg(arg_value, typ) for typ in get_args(arg_type))
        if get_origin(arg_type) is dict:
            key_type, val_type = get_args(arg_type)
            return all(RpcServer._valid_arg(key, key_type) for key in arg_value.keys()) and \
                all(RpcServer._valid_arg(val, val_type) for val in arg_value.values())
        return isinstance(arg_value, arg_type)

    @typechecked
    def _valid_inputs(self, queue: str, inputs: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        inputs_with_defaults = {**self._get_defaults(queue), **inputs}
        for arg_name, arg_type in self._get_input_types(queue).items():
            if arg_name not in inputs_with_defaults and not self._is_optional(arg_type):
                return False, f'Missing required argument {arg_name}'
            if arg_name in inputs_with_defaults and not self._valid_arg(inputs_with_defaults[arg_name], arg_type):
                return False, f'Invalid type for {arg_name}'
        return True, None

    @typechecked
    def register_rpc(self, queue: str,
                     callback: Callable,
                     register_docs: bool = True) -> None:
        self.channel.queue_declare(queue=queue, exclusive=False)
        self._callbacks[queue] = callback
        if register_docs:
            self._register_docs(queue, callback)
        # TODO: servers should have an exclusive Queue for information about themselves

        @typechecked
        def meta_callback(_, method, props: BasicProperties, body: bytes):
            req_id = props.correlation_id or uuid()
            with thread_name(req_id):
                log.debug('Request received')
                try:
                    try:
                        if valid_json(body.decode()):
                            input_args: Dict[str, Any] = from_json(body.decode())
                            log.debug(f'Input JSON is valid: {input_args}')
                            valid_inputs, msg = self._valid_inputs(queue, input_args)
                            if not valid_inputs:
                                log.debug('Invalid input')
                                response = RpcError(req_id, msg).to_json()
                            elif not input_args:
                                log.debug(f'Executing: {callback}')
                                response = RpcResponse(req_id, callback()).to_json()
                            else:
                                log.debug(f'Executing: {callback} with inputs: {input_args}')
                                response = RpcResponse(req_id, callback(**input_args)).to_json()
                        else:
                            response = RpcError(req_id,
                                                'Input could not be decoded as JSON').to_json()
                    except (AMQPError, ChannelError):
                        raise  # we want this kind of exception to be caught further down
                    except Exception:  # pylint: disable=W0703
                        log.error("An error has occurred during the execution of the RPC method")
                        for line in format_exc().split('\n'):
                            log.error(line)
                        response = RpcError(request_id=req_id, details=f'There was an error '
                                                                       f'while processing the '
                                                                       f'request, please refer '
                                                                       f'to server log with '
                                                                       f'request ID: '
                                                                       f'{req_id}').to_json()
                    log.debug(f'Response: {response}')
                    self.channel.basic_publish(exchange='',
                                               routing_key=props.reply_to,
                                               properties=BasicProperties(
                                                correlation_id=props.correlation_id),
                                               body=response)
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    log.debug('Response sent and ack-ed')
                except (AMQPError, ChannelError):
                    log.error(f"A RabbitMQ communication error has occurred while processing "
                              f"Request ID: {req_id}")
                    for line in format_exc().split('\n'):
                        log.error(line)
            if self.only_once:
                self.channel.stop_consuming()

        self.channel.basic_consume(queue=queue,
                                   on_message_callback=meta_callback,
                                   auto_ack=False)

    @retry(AMQPConnectionError, delay=2, jitter=1)
    @typechecked
    def run(self) -> None:
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            log.info("Shutting down server")
