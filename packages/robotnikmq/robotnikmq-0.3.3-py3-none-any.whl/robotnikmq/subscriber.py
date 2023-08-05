from collections import namedtuple
from traceback import format_exc
from typing import Optional, Callable, List, Generator

from pika.exceptions import AMQPConnectionError
from retry import retry
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, ConnErrorCallback, Message
from robotnikmq.error import MalformedMessage
from robotnikmq.log import log

OnMessageCallback = Callable[[Message], None]

ExchangeBinding = namedtuple('ExchangeBinding', ['exchange', 'binding_key'])


class Subscriber(Robotnik):
    @typechecked
    def __init__(self,
                 exchange_bindings: Optional[List[ExchangeBinding]] = None,
                 config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None):
        super().__init__(config=config, on_conn_error=on_conn_error)
        self.exchange_bindings = exchange_bindings or []
        self._halted = True

    @typechecked
    def _bind(self, exchange_binding: ExchangeBinding) -> 'Subscriber':
        self.exchange_bindings.append(exchange_binding)
        return self

    @typechecked
    def bind(self, exchange: str, binding_key: str = '#') -> 'Subscriber':
        return self._bind(ExchangeBinding(exchange, binding_key))

    @typechecked
    def stop(self) -> None:
        self._halted = True

    @retry(AMQPConnectionError, delay=2, jitter=1)
    @typechecked
    def run(self, callback: OnMessageCallback, inactivity_timeout: Optional[float] = None) -> None:
        self._halted = False
        while not self._halted:
            with self.open_channel() as channel:
                queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
                for ex_b in self.exchange_bindings:
                    channel.exchange_declare(exchange=ex_b.exchange,
                                             exchange_type='topic',
                                             auto_delete=True)
                    channel.queue_bind(exchange=ex_b.exchange,
                                       queue=queue_name,
                                       routing_key=ex_b.binding_key)
                for method, ___, body in channel.consume(queue=queue_name,  # pragma: no cover
                                                         auto_ack=False,
                                                         inactivity_timeout=inactivity_timeout):
                    if method and body:
                        callback(Message.of(body.decode()))
                        channel.basic_ack(delivery_tag=method.delivery_tag)
                    if self._halted:
                        break
                channel.cancel()
                self.close_channel(channel)

    @retry(AMQPConnectionError, delay=2, jitter=1)
    @typechecked
    def consume(self, inactivity_timeout: Optional[float] = None) -> Generator[Optional[Message],
                                                                               None, None]:
        with self.open_channel() as channel:
            queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
            for ex_b in self.exchange_bindings:
                channel.exchange_declare(exchange=ex_b.exchange,
                                         exchange_type='topic',
                                         auto_delete=True)
                channel.queue_bind(exchange=ex_b.exchange,
                                   queue=queue_name,
                                   routing_key=ex_b.binding_key)
            try:
                for method, ___, body in channel.consume(queue=queue_name,  # pragma: no cover
                                                         auto_ack=False,
                                                         inactivity_timeout=inactivity_timeout):
                    if method and body:
                        channel.basic_ack(delivery_tag=method.delivery_tag)
                        try:
                            yield Message.of(body.decode())
                        except MalformedMessage:
                            log.debug(format_exc())
                    else:
                        yield None
            finally:
                channel.cancel()
                self.close_channel(channel)
