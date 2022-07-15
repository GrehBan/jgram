from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from aiogram.types import ParseMode

from .. import exceptions
from .markup.markup import MarkupType, MarkupTypeLiteral, RawMarkup, RawMarkupType
from .media.media import MEDIA_TYPES, Media, MediaTypeLiteral


class ShowMode(Enum):
    SEND = auto()
    EDIT = auto()


class MediaDict(TypedDict):
    type: MediaTypeLiteral
    url: Optional[str]
    file_id: Optional[str]
    path: Optional[str]
    

class MarkupDict(TypedDict):
    type: MarkupTypeLiteral
    markup: RawMarkupType
    

class RawWindowReturnsDict(TypedDict):
    text: Optional[str]
    media: Optional[Media]
    parse_mode: Optional[str]
    web_preview: bool
    markup: Optional[MarkupType]


@dataclass(unsafe_hash=True)
class RawWindow:
    window_name: str
    text: Optional[str] = None
    media: Optional[MediaDict] = None
    parse_mode: Optional[str] = None
    web_preview: bool = True
    markup: Optional[MarkupDict] = None
    
    # helpers
    next_step: Optional[str] = None
    allowed_updates: List[Union[Literal["text"],
                                MediaTypeLiteral]] = field(default_factory=list)
    reset_context: bool = False
    filters: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        if self.allowed_updates \
            and not all((update == 'text' or 
                   update in MEDIA_TYPES 
                   for update in self.allowed_updates)):
            raise exceptions.InvalidWindowFieldsMap(
                "Unknown allowed updates list"
            )

    def build(self, context_data: Dict) -> RawWindowReturnsDict:
        text = self.text
        media = self.media
        parse_mode = self.parse_mode
        web_preview = self.web_preview
        markup = self.markup

        if text is None and media is None:
            raise exceptions.InvalidWindowFieldsMap(
                "Needs 'text' or 'media' field to show")
            
        if text is not None:
            text = text.format(**context_data)
        if media is not None:
            media = Media(**media)
            if not (
                media.file_id or
                media.url or
                media.path
            ):
                raise exceptions.InvalidWindowFieldsMap(
                    "Need's 'file_id' or 'url' or 'path' field "\
                    "in media map"
                )
            if media.type not in MEDIA_TYPES:
                raise exceptions.InvalidWindowFieldsMap(
                    f"Unknown media type {media.type!r}"
                )
        if parse_mode is not None:
            parse_mode = getattr(
                ParseMode, 
                parse_mode.upper(),
                None
                )
            if parse_mode is None:
                raise exceptions.InvalidWindowFieldsMap(
                    f"Unknown parse_mode {parse_mode!r}"
                )
        if markup is not None:
            markup = RawMarkup(**markup).build(context_data)

        return dict(
            text=text,
            media=media,
            parse_mode=parse_mode,
            web_preview=web_preview,
            markup=markup
        )


@dataclass(frozen=True)
class Window:
    mode: ShowMode
    chat_id: int
    text: Optional[str] = None
    media: Optional[Media] = None
    parse_mode: Optional[str] = None
    web_preview: bool = True
    markup: Optional[MarkupType] = None
