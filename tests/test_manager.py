import pytest

from jgram.exceptions import LocaleNotFoundError, WindowNotFoundError
from jgram.manager import WindowsManager
from jgram.window import RawWindow

from . import FakeLoader, FakeStorage, FakeWindow


class TestManager:
    manager = WindowsManager(storage=FakeStorage, loader=FakeLoader)
    
    @pytest.mark.asyncio
    async def test_manager_load_windows(self):
        self.manager.load_windows('')
        assert self.manager.windows == FakeLoader._json_
        
    @pytest.mark.asyncio
    async def test_manager_get_window(self):
        try:
            rt = self.manager.get_window('window_name', 'en')
            assert  isinstance(rt, RawWindow) and (
                rt.text == FakeWindow['text'] and
                rt.media is None and
                rt.parse_mode is None and
                rt.web_preview is True
            ) 
        except (LocaleNotFoundError, WindowNotFoundError):
            assert False
