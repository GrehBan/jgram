from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, Protocol


@dataclass
class StorageRecord:
    locale: Optional[str] = None
    window_name: Optional[str] = None
    data: Dict = field(default_factory=dict)


class StorageProto(Protocol):

    @abstractmethod
    async def close(self):
        pass
    
    @abstractmethod
    async def wait_closed(self):
        pass
    
    @abstractmethod
    async def get_data(self, user_id: int) -> Dict:
        pass
    
    @abstractmethod
    async def update_data(self, user_id: int, data: Optional[Dict] = None, **kwargs):
        pass
    
    @abstractmethod
    async def set_data(self, user_id: int, data: Dict):
        pass

    @abstractmethod
    async def reset_data(self, user_id: int):
        pass
    
    @abstractmethod
    async def get_user(self, user_id: int) -> StorageRecord:
        pass

    @abstractmethod
    async def get_locale(self, user_id: int) -> Optional[str]:
        pass
    
    @abstractmethod
    async def set_locale(self, user_id: int, locale: str):
        pass

    @abstractmethod
    async def set_window(self, user_id: int, window_name: str):
        pass
    
    @abstractmethod
    async def get_window(self, user_id: int) -> Optional[str]:
        pass


class BaseStorage(StorageProto):
    async def reset_data(self, user_id: int):
        await self.set_data(user_id=user_id, data={})
