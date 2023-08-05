from pathlib import Path
from random import choice
from ssl import create_default_context
from typing import Union, List, Optional, Dict, Any

from pika import ConnectionParameters, SSLOptions
from pika.credentials import PlainCredentials
from pydantic import BaseModel, validator
from typeguard import typechecked
from yaml import safe_load

from robotnikmq.error import ClientCertDoesNotExist, ClientKeyDoesNotExist, CACertDoesNotExist
from robotnikmq.error import NotConfigured
from robotnikmq.log import log


@typechecked
def _existing_file(path: Union[str, Path]) -> Path:
    try:
        path = Path(path).resolve()
        if not path.exists():
            raise ValueError(f'File path does not exist: {path}')
        return path
    except Exception as exc:
        raise ValueError(f'Invalid file path: {path}') from exc


class ServerConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    vhost: str
    ca_cert: Path
    cert: Path
    key: Path

    _existing_ca_cert = validator('ca_cert',
                                  pre=True,
                                  always=True,
                                  allow_reuse=True)(_existing_file)
    _existing_cert = validator('cert',
                               pre=True,
                               always=True,
                               allow_reuse=True)(_existing_file)
    _existing_key = validator('key',
                              pre=True,
                              always=True,
                              allow_reuse=True)(_existing_file)

    class Config:
        json_encoders = {
            Path: str,
        }


@typechecked
def server_config(host: str, port: int, user: str, password: str, vhost: str,
                  ca_cert: Union[str, Path], cert: Union[str, Path],
                  key: Union[str, Path]) -> ServerConfig:
    ca_cert, cert, key = Path(ca_cert), Path(cert), Path(key)
    if not ca_cert.is_file():
        raise CACertDoesNotExist(ca_cert)
    if not cert.is_file():
        raise ClientCertDoesNotExist(cert)
    if not key.is_file():
        raise ClientKeyDoesNotExist(key)
    return ServerConfig(host=host, port=port, user=user, password=password,
                        vhost=vhost, ca_cert=ca_cert, cert=cert, key=key)


@typechecked
def conn_params_of(config: ServerConfig) -> ConnectionParameters:
    context = create_default_context(cafile=str(config.ca_cert))
    context.load_cert_chain(config.cert, config.key)
    return ConnectionParameters(host=config.host,
                                port=config.port,
                                virtual_host=config.vhost,
                                credentials=PlainCredentials(config.user, config.password),
                                ssl_options=SSLOptions(context, config.host))


class RobotnikConfig(BaseModel):
    tiers: List[List[ServerConfig]]

    @typechecked
    def tier(self, index: int) -> List[ServerConfig]:
        return self.tiers[index]

    @typechecked
    def a_server(self, tier: int) -> ServerConfig:
        return choice(self.tier(tier))

    @typechecked
    def as_dict(self) -> Dict[str, Any]:
        return self.dict()


@typechecked
def config_of(config_file: Optional[Path]) -> RobotnikConfig:
    if config_file is None or not config_file.exists():
        log.critical("No valid RobotnikMQ configuration file was provided")
        raise NotConfigured("No valid RobotnikMQ configuration file was provided")
    return RobotnikConfig(**safe_load(config_file.open().read()))
