from abc import abstractmethod
from typing import IO, Dict, Protocol, Union

from .. import _types, json

LoadedWindows = Dict[str, json.LoadedJson]


class LoaderProto(Protocol):
    @abstractmethod
    def load_json(self, fp: Union[_types.PathLike, IO[bytes]]) -> LoadedWindows:
        pass
