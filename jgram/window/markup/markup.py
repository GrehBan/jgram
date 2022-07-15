from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Type, TypedDict, Union

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from jgram import exceptions

from . import tools

ReplyButtonDict = TypedDict(
    'ReplyButtonDict',
    {
        'text': str,
        'request_contact': Optional[bool],
        'request_location': Optional[bool]
    }
)

InlineButtonDict = TypedDict(
    'InlineButtonDict',
    {
        'text': str,
        'callback_data': Optional[str],
        'url': Optional[str],
        'login_url': Optional[str],
        'switch_inline_query': Optional[str],
        'switch_inline_query_current_chat': Optional[str],
        'pay': Optional[bool],
    }
)
MarkupType = Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
RawMarkupType = List[List[Union[InlineButtonDict, ReplyButtonDict]]]
MarkupTypeLiteral = Union[Literal["type"], Literal["inline"]]


@dataclass
class RawMarkup:
    markup: RawMarkupType
    type: MarkupTypeLiteral

    def _build(self, 
               formatting: Dict, 
               markup_class: Type[MarkupType],
               button_class: Type[Union[InlineKeyboardButton, KeyboardButton]])\
                   -> MarkupType:
                       
        markup = markup_class()
        if isinstance(markup, InlineKeyboardMarkup):
            raw_markup = markup.inline_keyboard
        else:
            raw_markup = markup.keyboard

        for row in self.markup.copy():
            raw_markup.append([])
            for button in row:
                try:
                    raw_markup[-1].append(
                        button_class(
                        **tools.apply_formatting_to_map(
                            button, formatting
                            )
                        ))
                except TypeError as e:
                    raise exceptions.InvalidWindowFieldsMap(
                        f"Invalid markup button map {button!r}"
                    ) from e
        markup.row_width = max(raw_markup)
        return markup
    
    def build(self, formatting: Dict) -> MarkupType:
        if self.type == 'inline':
            return self._build(formatting,
                               InlineKeyboardMarkup,
                               InlineKeyboardButton)
        elif self.type == 'reply':
            return self._build(formatting,
                                ReplyKeyboardMarkup,
                                KeyboardButton)
        raise exceptions.InvalidWindowFieldsMap(
            f"Invalid markup type {self.type!r}"
        )

