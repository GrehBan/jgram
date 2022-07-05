from typing import TYPE_CHECKING, Dict, Union

from aiogram.dispatcher.filters import Filter
from aiogram.types.base import TelegramObject

from ..storage.protocols import BaseStorage

if TYPE_CHECKING:
    from .registry import Registry
    

class IncludeData(Filter):
    def __init__(self, registry: 'Registry') -> None:
        super().__init__()
        self._registry = registry
        
    async def check(self, update: TelegramObject, *args) -> Union[bool, Dict]:
        user = await self._registry.manager.storage.get_user(user_id=update.from_user.id)
        return {'window_name': user.window_name, 
                'user': user,
                'registry': self._registry}
