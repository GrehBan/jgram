from __future__ import annotations

from typing import Callable, Optional

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.handler import Handler

from ..loggers import registry_logger
from ..manager import WindowsManager
from .filters import HaveWindowFilter, IncludeRegistry
from .handlers.start import start_handler
from .handlers.update import update_handler
from .middleware import ProcessMiddleware
from .protocols import RegistryProto


class Registry(RegistryProto):
    def __init__(self,
                 bot: Optional[Bot] = None,
                 dispatcher: Optional[Dispatcher] = None,
                 token: Optional[str] = None,
                 manager: Optional[WindowsManager] = None):

        if bot is None and dispatcher is None and token is None:
            raise ValueError('Need\'s `bot`, `dispatcher` or `token` to initialize')
        elif dispatcher is not None:
            bot = dispatcher.bot
        elif bot is not None:
            dispatcher = Dispatcher(bot=bot)
        else:
            bot = Bot(token=token)
            dispatcher = Dispatcher(bot=bot)

        if manager is None:
            manager = WindowsManager()
            
        self._bot = bot
        self._dispatcher = dispatcher

        self._manager = manager
        self._middlewares = ProcessMiddleware()

        have_window = HaveWindowFilter(self.manager.storage)
        include_registry = IncludeRegistry(self)

        # register update handlers
        # insert it to first positions
        self.register_update_handler(start_handler,
                                     self.dispatcher.message_handlers,
                                     include_registry, 
                                     commands=['start']) # start all dialogs from this handler
        self.register_update_handler(update_handler, 
                                     self.dispatcher.message_handlers,
                                     have_window, 
                                     include_registry,
                                     index=1) # index 1 because start_handler added to index 0
        self.register_update_handler(update_handler,
                                     self.dispatcher.callback_query_handlers,
                                     have_window,
                                     include_registry,
                                     index=0)

    def register_update_handler(self,
                                callback: Callable,
                                handler: Handler,
                                *filters, 
                                index: int = 0,
                                **kw_filters):
        filters_set = self.dispatcher.filters_factory.resolve(
            handler,
            *filters,
            **kw_filters
        )
        handler.register(callback, filters_set, index=index)
    
    @property
    def bot(self) -> Bot:
        return self._bot
    
    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher
    
    @property
    def manager(self) -> WindowsManager:
        return self._manager
    
    def register_middleware(self, callback: Callable, name: Optional[str] = None):
        self._middlewares.register(callback, name)
    
    def middleware(self, name: Optional[str] = None):
        def decorator(callback: Callable):
            self.register_middleware(callback, name)
            return callback
        return decorator

    async def start(self):
        await self.dispatcher.start_polling()

    async def close(self):
        session = await self.bot.get_session()
        await session.close()
        await self.dispatcher.storage.close()
        await self.dispatcher.storage.wait_closed()
        await self.manager.close()

        registry_logger.info('all closed')
