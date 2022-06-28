from typing import TYPE_CHECKING, Dict, Union

from aiogram.dispatcher.filters import Filter
from aiogram.types.base import TelegramObject

from ..storage.protocols import BaseStorage

if TYPE_CHECKING:
    from .registry import Registry
    

class HaveWindowFilter(Filter):
    def __init__(self, storage: BaseStorage):
        self._storage = storage
        
    async def check(self, update: TelegramObject, *args) -> Union[bool, Dict]:
        user = await self._storage.get_user(user_id=update.from_user.id, 
                                                 create_user=True)
        user_data = user['data']
        window_name = user_data['window_name']
        if bool(window_name) is True:
            return {'window_name': window_name, 'user': user}
        return False
    

class IncludeRegistry(Filter):
    def __init__(self, registry: 'Registry') -> None:
        super().__init__()
        self._registry = registry
                
    async def check(self, *args) -> Dict:
        return {'registry': self._registry}
