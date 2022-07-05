from typing import TYPE_CHECKING

from aiogram.types import Message

from jgram.storage.protocols import StorageRecord

from .update import update_handler

if TYPE_CHECKING:
    from ..registry import Registry
    

async def start_handler(message: Message, window_name: str, user: StorageRecord, registry: 'Registry'):
    return await update_handler(
        update=message,
        registry=registry,
        window_name=registry.manager._start_window,
        user=user,
        build_next_step=False
    )
