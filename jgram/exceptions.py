from typing import Any, Dict, Optional, Tuple


class JgramError(Exception):
    message: str = ''

    def __init__(self,
                 message: Optional[str] = None,
                 *args: Tuple[Any],
                 **message_format_kwargs: Dict[str, Any]) -> None:
        if message is None:
            message = self.message
        message = message.format(**message_format_kwargs)
        super().__init__(message, *args)


class JsonLoaderError(JgramError):
    pass


class ManagerError(JgramError):
    pass


class JsonProcessError(JgramError):
    pass


class TextBuildError(JgramError):
    pass


class InvalidJsonFormat(JsonLoaderError, ValueError):
    message: str = 'invalid format of json file {file_name!r}'


class InvalidFileType(JsonLoaderError, ValueError):
    message: str = 'file to load must be a json type file, not {file_type!r}'


class NotLoadedError(ManagerError):
    message: str = 'trying to get texts before load it'


class LocaleNotFoundError(ManagerError):
    message: str = 'locale {locale_name!r} not found'


class WindowNotFoundError(ManagerError):
    message: str = 'window {window_name!r} not found'


class InvalidProcessedFormat(JsonProcessError):
    pass


class InvalidWindowFieldsMap(TextBuildError):
    pass
