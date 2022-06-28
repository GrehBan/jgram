from copy import deepcopy
from typing import Any, Dict, Optional, Union

from .protocols import BaseStorage


class MemoryStorage(BaseStorage):
    
    async def close(self):
        self._storage.clear()
    
    async def wait_closed(self):
        pass
    
    def __init__(self):
        self._storage: Dict[str, Union[Any, Dict]] = dict()
    
    async def get_user(self, user_id: int, create_user: bool = False, no_error: bool = False) -> Dict:
        user = self._storage.get(user_id)
        if user is None:
            return await self.load_user(user_id, create_user, no_error)
        return user
    
    async def get_data(self, user_id: int, create_user: bool = False, no_error: bool = False) -> Dict:
        user = await self.get_user(user_id, create_user, no_error)
        return deepcopy(user['data'])
    
    async def update_data(self, user_id: int, create_user: bool = False, data: Optional[Dict] = None, **kwargs):
        
        if create_user is True and user_id not in self._storage:
            await self.create_user(user_id)
        if user_id not in self._storage:
            raise ValueError(f'User with {user_id} id not found in storage')
        
        if data is None:
            data = {}
        self._storage[user_id]['data'].update(data, **kwargs)
        
    async def set_data(self, user_id: int, data: Dict, create_user: bool = False):
        
        if create_user is True and user_id not in self._storage:
            await self.create_user(user_id=user_id)
        if user_id not in self._storage:
            raise ValueError(f'User with {user_id} id not found in storage')
        if 'window_name' not in data:
            data['window_name'] = None
            
        self._storage[user_id]['data'] = data
        
    async def create_user(self, user_id: int) -> Dict:
        created = dict(
            locale=None,
            data=dict(
                window_name=None
            )
        )
        self._storage[user_id] = deepcopy(created)
        return created

    async def delete_user(self, user_id: int):
        self._storage.pop(user_id, None)

    async def set_locale(self, user_id: int, locale: str, create_user: bool = False):
        user = await self.get_user(user_id, create_user)
        user['locale'] = locale
        
    async def get_locale(self, user_id: int, create_user: bool = False) -> Optional[str]:
        if create_user is True and user_id not in self._storage:
            await self.create_user(user_id)
        if user_id not in self._storage:
            raise ValueError(f'User with {user_id} id not found in storage')
        
        return self._storage[user_id]['locale']
