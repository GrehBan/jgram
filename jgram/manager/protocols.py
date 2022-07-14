from abc import abstractmethod
from typing import IO, Dict, Optional, Protocol, Union

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from ..storage.protocols import BaseStorage
from ..window.window import RawWindow, ShowMode, Window


class ManagerProto(Protocol):
    
    @abstractmethod
    async def close(self):
        pass
    
    @property
    @abstractmethod
    def storage(self) -> BaseStorage:
        pass

    @abstractmethod
    async def show_window(self, bot: Bot, text: Window, 
                        old_message: Optional[Message] = None) -> Message:
        pass
    
    @abstractmethod
    def load_windows(self, fp: Union[str, IO[bytes]]):
        pass

    @abstractmethod
    def get_window(self, name: str, locale: str) -> RawWindow:
        pass
    
    @abstractmethod
    async def update_window(self,
                          update: Union[Message, CallbackQuery],
                          locale: str,
                          context_data: Dict,
                          mode: ShowMode,
                          name: Optional[str] = None,
                          raw_window: Optional[RawWindow] = None,
                          ) -> Window:
        pass
