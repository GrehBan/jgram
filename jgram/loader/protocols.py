from abc import abstractmethod
from typing import IO, Any, Dict, Protocol, Union

from .. import _types


class LoaderProto(Protocol):
    @abstractmethod
    def load_windows(self, fp: Union[_types.PathLike, IO[bytes]]) -> Dict[str, Any]:
        pass
