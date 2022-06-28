from typing import TYPE_CHECKING

from aiogram.types import Message

from .update import update_handler

if TYPE_CHECKING:
    from ..registry import Registry
    

async def start_handler(message: Message, registry: 'Registry'):
    return await update_handler(
        update=message,
        registry=registry,
        window_name=registry.manager._start_window,
        user=await registry.manager.storage.get_user(
            user_id=message.from_user.id,
            create_user=True
        ),
        build_next_step=False
    )
