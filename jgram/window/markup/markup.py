from dataclasses import dataclass
from typing import Dict, List, Type, Union

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from jgram import exceptions

from . import tools

MarkupType = Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
RawMarkupType = List[List[Dict]]


@dataclass
class RawMarkup:
    markup: RawMarkupType
    type: str

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

