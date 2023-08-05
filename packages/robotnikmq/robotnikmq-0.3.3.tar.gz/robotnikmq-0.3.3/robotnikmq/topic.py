import json
from typing import Optional

from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, Message, ConnErrorCallback, AMQPErrorCallback
from robotnikmq.log import log


class Topic(Robotnik):
    @typechecked
    def __init__(self, exchange: str,
                 config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None):
        super().__init__(config=config, on_conn_error=on_conn_error)
        self.exchange = exchange
        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type='topic',
                                      auto_delete=True)

    @typechecked
    def broadcast(self, msg: Message,
                  routing_key: Optional[str] = None,
                  on_msg_error: AMQPErrorCallback = None) -> None:
        msg.routing_key = routing_key or msg.routing_key
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=(routing_key or msg.routing_key or ''),
                                   body=json.dumps(msg.to_dict()))
        log.debug(f'Broadcast: \n{json.dumps(msg.to_dict(), indent=4)}')
