from __future__ import annotations

from typing import IO, Any, BinaryIO, Dict, Optional, Union

from aiogram import Bot
from aiogram.types import CallbackQuery, InputMedia, Message
from aiogram.utils.exceptions import (
    MessageCantBeDeleted,
    MessageCantBeEdited,
    MessageNotModified,
    MessageToDeleteNotFound,
    MessageToEditNotFound,
)

from .. import exceptions
from ..loader import JsonLoader, LoaderProto
from ..loggers import manager_logger
from ..storage.memory import MemoryStorage
from ..storage.protocols import BaseStorage
from ..window.media import MEDIA_TYPES, Media
from ..window.window import RawWindow, ShowMode, Window
from .protocols import ManagerProto


class WindowsManager(ManagerProto):
    """
    Windows manager
    """
    def __init__(self,
                 storage: Optional[BaseStorage] = None,
                 loader: Optional[LoaderProto] = None,
                 start_window: str = 'start'
                 ):
        """
        Windows manager

        :param storage: jgram's users data storage, defaults to None
        :param loader: jgram's window loader, defaults to None
        :param start_window: name of window for render on /start command, defaults to 'start'
        """
        if storage is None:
            storage = MemoryStorage()
            manager_logger.debug(
                f'Initialized {type(storage).__name__} '
                'because `storage` was not set'
            )
        if type(storage) == MemoryStorage:
            manager_logger.warning(
                'You use MemoryStorage '
                'so data dont be saved permanently'
                )
        
        
        if loader is None:
            loader = JsonLoader()
            manager_logger.debug(
                f'Initialized {type(loader).__name__} '
                'because `loader` was not set'
            )
        
        self._loader = loader
        self._windows: Dict[str, Any] = {}
        self._storage = storage
        self._start_window = start_window
        
    async def close(self):
        """
        Close storage and clear windows
        """
        await self.storage.close()
        await self.storage.wait_closed()
        self._windows.clear()
        manager_logger.debug(
            'storage closed and windows deleted'
        )
    
    @property
    def windows(self) -> Dict[str, Any]:
        if not self._windows:
            raise exceptions.NotLoadedError()
        return self._windows
    
    @property
    def storage(self) -> BaseStorage:
        return self._storage
    
    @property
    def default_locale(self) -> str:
        """
        Get default locale
        if default locale not found, getting first key
        of loaded windows, and return it

        :return: ISO locale string
        """
        if self._loader._default_locale:
            return self._loader._default_locale
        manager_logger.debug(
            'getting first key of loaded windows dict, '
            'and using it as default locale '
            'because it not set'
        )
        return next(iter(self.windows))

    def load_windows(self, fp: Union[str, IO]):
        """
        alias for jgram's loader .load_windows with saving loaded data

        :param fp: path or file-like decsriptor to load
        """
        self._windows = self._loader.load_windows(fp=fp)

    def get_window(self, name: str, locale: str) -> RawWindow:
        """
        Get window by name and locale

        :param name: window name
        :param locale: locale of window
        :raises exceptions.LocaleNotFoundError: if locale not found
        :raises exceptions.WindowNotFoundError: if window not founc
        :return: jgram's loaded window dataclass
        """
        windows = self.windows.get(locale)
        if windows is None:
            raise exceptions.LocaleNotFoundError(locale_name=name)
        window = windows.get(name)
        if window is None:
            raise exceptions.WindowNotFoundError(window_name=name)
        
        return RawWindow(name, **window)

    def get_media_source(self, media: Media) -> Union[str, BinaryIO]:
        if media.file_id:
            return media.file_id
        elif media.url:
            return media.url
        else:
            return open(media.path, 'rb')
        
    async def update_window(self,
                          update: Union[Message, CallbackQuery],
                          locale: str, 
                          context_data: Dict,
                          mode: ShowMode,
                          name: Optional[str] = None,
                          raw_window: Optional[RawWindow] = None) -> Window:
        """
        Switch current window to new, and update data
        
        :param update: aiogram's update
        :param locale: window locale
        :param context_data: context data
        :param mode: window show mode, `SEND` or `EDIT`
        :param name: window name, defaults to None
        :param raw_window: jgram's raw window object, defaults to None
        :raises ValueError: if `name` or `raw_window` fields not passed
        :return: jgram's builded window dataclass
        """
        if not name and not raw_window:
            raise ValueError(
                "Need's `raw_window` or `name` to update window"
            )
            
        old_message = update
        if isinstance(old_message, CallbackQuery):
            old_message = old_message.message
        
        if not raw_window: 
            raw_window = self.get_window(name, locale)
        window = Window(
            mode=mode,
            chat_id=update.from_user.id,
            **raw_window.build(context_data)
        )
        await self.show_window(bot=update.bot, window=window, old_message=old_message)
        await self.storage.set_window(user_id=update.from_user.id,
                                       window_name=raw_window.window_name)
        return window
    
    # window show logic from https://github.com/tishka17/aiogram_dialog/
    async def show_window(self, bot: Bot, 
                        window: Window, 
                        old_message: Optional[Message] = None) -> Message:
        if old_message is None or window.mode == ShowMode.SEND:
            manager_logger.debug(
                'send new message '
                f'because old_message mode is {window.mode} and '
                f'old message is {old_message}'
            )
            await self.remove_markup(bot=bot, 
                                     old_message=old_message)
            return await self.send_window(bot=bot, window=window)
        
        have_media = old_message.content_type in MEDIA_TYPES
        need_media = window.media is not None
        
        if (
            old_message.text == window.text and
            old_message.reply_markup == window.markup and
            have_media == need_media and 
            not need_media
        ):
            return old_message
        if have_media != need_media:
            try:
                await bot.delete_message(
                    chat_id=old_message.chat.id,
                    message_id=old_message.message_id
                )
            except (MessageCantBeDeleted, MessageToDeleteNotFound):
                await self.remove_markup(bot=bot, old_message=old_message)
            return await self.send_window(bot=bot, window=window)
        
        try:
            return await self.edit_window(bot=bot, window=window, old_message=old_message)
        except MessageNotModified:
            return old_message
        except (MessageCantBeEdited, MessageToEditNotFound):
            return await self.send_window(bot=bot, window=window)
    
        
    async def remove_markup(self, bot: Bot, old_message: Optional[Message] = None) -> Optional[Message]:
        if old_message is not None:
            manager_logger.debug(
                f'remove keyboard in {old_message.chat}'
            )
            try:
                return await bot.edit_message_reply_markup(
                    chat_id=old_message.chat.id,
                    message_id=old_message.message_id
                )
            except (MessageNotModified, MessageCantBeEdited,
                        MessageToEditNotFound):
                pass

    # send
    async def send_window(self, bot: Bot, window: Window) -> Message:
        if window.media:
            await self.send_media(bot, window)
        else:
            await self.send_message(bot, window)
    
    async def send_message(self, bot: Bot, window: Window) -> Message:
        return await bot.send_message(
            chat_id=window.chat_id,
            text=window.text,
            disable_web_page_preview=not window.web_preview,
            parse_mode=window.parse_mode,
            reply_markup=window.markup
        )
    
    async def send_media(self, bot: Bot, window: Window) -> Message:
        method = MEDIA_TYPES[window.media.type].get_method(bot)
        return await method(
            window.chat_id,
            self.get_media_source(window.media),
            caption=window.text,
            reply_markup=window.markup,
            parse_mode=window.parse_mode,
            **window.media.kwargs
        )
        
    # edit
    async def edit_window(self, bot: Bot, window: Window, old_message: Message) -> Message:
        if window.media:
            old_message_media_id = MEDIA_TYPES[window.media.type].get_file_id(old_message)
            if (
                old_message_media_id is not None and
                window.media.file_id == old_message_media_id
                ):
                return await self.edit_caption(bot, window, old_message)
            return await self.edit_media(bot, window, old_message)
        else:
            return await self.edit_message(bot, window, old_message)
    
    async def edit_message(self, bot: Bot, window: Window, old_message: Message) -> Message:
        return await bot.edit_message_text(
            message_id=old_message.message_id,
            chat_id=window.chat_id,
            text=window.text,
            parse_mode=window.parse_mode,
            disable_web_page_preview= not window.web_preview,
            reply_markup=window.markup
        )
    
    async def edit_caption(self, bot: Bot, window: Window, old_message: Message) -> Message:
        return await bot.edit_message_caption(
            chat_id=old_message.chat.id,
            message_id=old_message.message_id,
            caption=window.text,
            parse_mode=window.parse_mode,
            reply_markup=window.markup
        )

    async def edit_media(self, bot: Bot, window: Window, old_message: Message) -> Message:
        media = InputMedia(
            caption=window.text,
            reply_markup=window.markup,
            parse_mode=window.parse_mode,
            disable_web_page_preview= not window.web_preview
        )
        return await bot.edit_message_media(
            message_id=old_message.message_id,
            chat_id=window.chat_id,
            media=media,
            reply_markup=window.markup
        )
