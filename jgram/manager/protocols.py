from abc import abstractmethod
from typing import IO, Awaitable, Callable, Dict, List, Optional, Protocol, Tuple, Union

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import AbstractFilter
from aiogram.types import CallbackQuery, Message

from ..storage.protocols import BaseStorage
from ..window.window import RawWindow, ShowMode, Window

FilterFunc = Callable[[Union[Message, CallbackQuery]], Optional[Union[bool, Dict]]]
FiltersList = List[Union[Union[FilterFunc,
                               Awaitable[FilterFunc]], 
                         AbstractFilter]]


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


class FiltersFactoryProto(Protocol):
    @property
    @abstractmethod
    def dispatcher(self) -> Dispatcher:
        pass

    @abstractmethod
    def build(self, filters: Dict) -> Tuple[str, FiltersList]:
        pass

    @abstractmethod
    async def check(self, filters_list: FiltersList) -> Union[Dict, bool]:
        pass
