from json import JSONEncoder, dumps
from pathlib import Path
from typing import Any

from typeguard import typechecked


class MyEncoder(JSONEncoder):  # pragma: no cover # not directly used in code
    @typechecked
    def default(self, obj: Any) -> Any:  # pylint: disable=W0221
        if isinstance(obj, Path):
            return str(obj)
        return JSONEncoder.default(self, obj)


@typechecked
def to_json(obj: Any) -> Any:
    return dumps(obj, cls=MyEncoder)
