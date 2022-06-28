from abc import abstractmethod
from ctypes import Union
from typing import Dict, Optional, Protocol


class StorageProto(Protocol):

    @abstractmethod
    async def close(self):
        pass
    
    @abstractmethod
    async def wait_closed(self):
        pass
    
    @abstractmethod
    async def get_data(self, user_id: int, create_user: bool = False) -> Dict:
        pass
    
    @abstractmethod
    async def update_data(self, user_id: int, create_user: bool = False, data: Optional[Dict] = None, **kwargs):
        pass
    
    @abstractmethod
    async def set_data(self, user_id: int, data: Dict, create_user: bool = False):
        pass

    @abstractmethod
    async def reset_data(self, user_id: int, create_user: bool = False):
        pass
    
    @abstractmethod
    async def get_user(self, user_id: int, create_user: bool = False) -> Dict:
        pass
    
    @abstractmethod
    async def create_user(self, user_id: int) -> Dict:
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: int):
        pass

    @abstractmethod
    async def get_locale(self, user_id: int, create_user: bool = False) -> Optional[str]:
        pass
    
    @abstractmethod
    async def set_locale(self, user_id: int, locale: str, create_user: bool = False):
        pass

    @abstractmethod
    async def set_window(self, user_id: int, window_name: str, create_user: bool = False):
        pass
    
    @abstractmethod
    async def get_window(self, user_id: int, create_user: bool = False) -> Optional[str]:
        pass
    
    @abstractmethod
    async def check_user(self, user_id: int, create_user: bool = False) -> bool:
        pass


class BaseStorage(StorageProto):
    async def reset_data(self, user_id: int, create_user: bool = False):
        await self.set_data(user_id=user_id, create_user=create_user, data={})
