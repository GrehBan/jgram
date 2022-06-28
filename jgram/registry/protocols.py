from abc import abstractmethod
from typing import Protocol

from ..manager.protocols import ManagerProto


class RegistryProto(Protocol):
    @abstractmethod
    async def start(self):
        pass
    
    @abstractmethod
    async def close(self):
        pass

    @property
    @abstractmethod
    def manager(self) -> ManagerProto:
        pass


