from abc import abstractmethod
from typing import IO, Any, Dict, Protocol, Union


class LoaderProto(Protocol):
    @abstractmethod
    def load_windows(self, fp: Union[str, IO]) -> Dict[str, Any]:
        """
        Load windows from path or file-like descriptor

        :param fp: path or file-like descriptor
        :return: loaded windows
        """
        pass
