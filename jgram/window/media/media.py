from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

from aiogram import Bot
from aiogram.types import ContentType, File, Message

from jgram import _types


@dataclass
class MediaType:
    method: str
    type_name: str
    
    def get_method(self, bot: Bot) -> Callable:
        return getattr(bot, self.method)

    def get_message_field(self, message: Message) -> Optional[File]:
        return getattr(message, self.type_name, None)

    def get_file_id(self, message: Message) -> Optional[str]:
        field = self.get_message_field(message=message)
        if field is not None:
            return field.file_id


MEDIA_TYPES = {
    ContentType.ANIMATION: MediaType(
        method='send_animation',
        type_name='animation'
    ),
    ContentType.AUDIO: MediaType(
        method='send_audio',
        type_name='audio'
        ),
    ContentType.DOCUMENT: MediaType(
        method='send_document',
        type_name='document'
        ),
    ContentType.PHOTO: MediaType(
        method='send_photo',
        type_name='photo'
    ),
    ContentType.VIDEO: MediaType(
        method='send_vide',
        type_name='video'
        ),
}


@dataclass
class Media:
    type: str
    url: Optional[_types.PathLike] = None
    file_id: Optional[str] = None
    path: Optional[_types.PathLike] = None
    kwargs: Dict = field(default_factory=dict)
