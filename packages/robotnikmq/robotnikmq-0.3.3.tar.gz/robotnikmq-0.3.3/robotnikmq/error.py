from pathlib import Path
from typing import Union


class UnableToConnect(Exception):
    def __str__(self):
        return f'{self.__class__.__name__}: Robotnik is unable to connect: {self.args}'


class MalformedMessage(Exception):
    def __init__(self, msg_input: str):
        self.malformed_input = msg_input
        super().__init__()

    def __str__(self):
        return f'Unable to decode RobotnikMQ message from: "{self.malformed_input}"'


class FileDoesNotExist(Exception):
    msg = 'Cannot find'

    def __init__(self, path: Union[Path, str]):
        self.path = path
        super().__init__()

    def __str__(self):
        return f'{self.__class__.__name__}: {self.msg} {self.path}'


class CACertDoesNotExist(FileDoesNotExist):
    msg = 'CA Certificate file not found:'


class ClientCertDoesNotExist(FileDoesNotExist):
    msg = 'Client Certificate file not found:'


class ClientKeyDoesNotExist(FileDoesNotExist):
    msg = 'Client Private Key file not found:'


class NotConfigured(Exception):
    msg = 'Robotnik is not configured'
