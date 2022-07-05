from collections import defaultdict
from typing import DefaultDict, Dict, Optional

from .protocols import BaseStorage, StorageRecord


class MemoryStorage(BaseStorage):
    
    async def close(self):
        self._storage.clear()
    
    async def wait_closed(self):
        pass
    
    def __init__(self):
        self._storage: DefaultDict[int, StorageRecord] = defaultdict(
            StorageRecord
        )
    
    async def get_user(self, user_id: int) -> StorageRecord:
        return self._storage[user_id]
    
    async def get_data(self, user_id: int) -> Dict:
        return self._storage[user_id].data
    
    async def update_data(self, user_id: int, data: Optional[Dict] = None, **kwargs):
        
        if data is None:
            data = {}
        self._storage[user_id].data.update(data, **kwargs)
        
    async def set_data(self, user_id: int, data: Dict):
        
        self._storage[user_id].data = data

    async def set_locale(self, user_id: int, locale: str):
        self._storage[user_id].locale = locale
        
    async def get_locale(self, user_id: int) -> Optional[str]:
        return self._storage[user_id].locale

    async def set_window(self, user_id: int, window_name: str):
        self._storage[user_id].window_name = window_name
    
    async def get_window(self, user_id: int) -> Optional[str]:
        return self._storage[user_id].window_name
