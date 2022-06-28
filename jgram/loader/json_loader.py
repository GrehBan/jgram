import os
import os.path
from io import TextIOBase
from typing import IO, Optional, Tuple, Union

from .. import _types, exceptions, json
from ..loggers import loader_logger
from . import tools
from .protocols import LoadedWindows, LoaderProto


class JsonLoader(LoaderProto):
    
    def __init__(self, default_locale: Optional[str] = 'en'):
        self._default_locale = default_locale
        
        if self._default_locale is None:
            loader_logger.warning(
                '`default_locale` was set to None '\
                'for loading windows '\
                'all of them must have a \'locale\' field'
            )
        
    def load_from_stream(self, stream: IO[bytes]) -> Tuple[str, json.LoadedJson]:
        try:
            loaded_json = json.load(stream)
        except json.DecodeError as e:
            raise exceptions.InvalidJsonFormat(
                file_name=tools.abspath(stream.name)
                ) from e
        
        locale = loaded_json.pop('locale', self._default_locale)
        if locale is None:
            raise exceptions.InvalidProcessedFormat(
                'field \'locale\' was not found '\
                'and `default_locale` was not set'
            )
        return locale, loaded_json
    
    def load_from_file(self, fp: _types.PathLike) -> Tuple[str, json.LoadedJson]:

        info = fp.split('.')
        
        if len(info) < 2:
            suff = ''
        else:
            suff = info[-1]
            
        if suff != 'json':
            raise exceptions.InvalidFileType(file_type=suff)
        
        with open(fp, 'rb') as fio:
            return self.load_from_stream(fio)
  
    def load_from_dir(self, dp: _types.PathLike) -> LoadedWindows:
        loaded_windows = {}
        for fp in tools.iterdir(dp):
            locale, loaded_json = self.load_from_file(fp)
            loaded_windows[locale] = loaded_json
            
        return loaded_windows
        
    def load_json(self, fp: Union[_types.PathLike, IO[bytes]]) -> LoadedWindows:
        
        loaded_windows: LoadedWindows = dict()
        
        if isinstance(fp, str):
            fp = tools.abspath(fp)
            
            if os.path.isdir(fp):
                loaded_windows.update(self.load_from_dir(fp))
                
                return loaded_windows
            
            elif os.path.isfile(fp):
                locale, loaded_json = self.load_from_file(fp)
                loaded_windows[locale] = loaded_json
            
                return loaded_windows
        
        elif isinstance(fp, TextIOBase):
            locale, loaded_json = self.load_from_stream(fp)
            loaded_windows[locale] = loaded_json
            
            return loaded_windows
        
        raise ValueError(
            f'Argument `fp` must be a valid file path or '\
            f'file-like descriptor, not `{type(fp).__name__}`'
            )
