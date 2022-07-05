import os.path
from collections import namedtuple

from aiogram import Bot

WORK_DIR = os.path.dirname(__file__)


User = namedtuple('User', 'id')
Chat = namedtuple('Chat', 'id')
Update = namedtuple('Update', 'from_user')
Context = namedtuple('Context', 'locale user_id data')
RawWindow = namedtuple('RawWindow', 'window_name reset allowed_updates next_step clear')
StorageRecord = namedtuple('StorageRecord', 'locale window_name user_id data')

FakeUser = User(id=0)
FakeChat = Chat(id=0)
FakeMessage = Update(from_user=FakeUser)
FakeBot = Bot(token='0:0', validate_token=False)
FakeContext = Context('en', FakeUser.id, {})
FakeRawWindow = RawWindow('start', False, None, None, False)
FakeRecord = StorageRecord(None, None, FakeUser.id, {})


class Storage:
    _user = StorageRecord('en', 'window_name', FakeUser.id, {})
    
    def __init__(self, empty: bool = False):
        self._empty = empty
    
    async def get_user(self, *a, **kw):
        if self._empty:
            return FakeRecord
        return self._user
    
    async def get_data(self, *a, **kw):
        return self._user.data
    
    async def close(self):
        pass

    async def wait_cloed(self):
        pass
    

FakeWindow = {
    "text": "ok"
}


class Loader:
    _json_ = {
            'en': {
                "window_name": FakeWindow
            }
        }

    def load_windows(self, *args, **kwargs):
        return self._json_


class Middleware:
    async def process(self, *args, **kwargs):
        pass
    
    
class Registry:
    def __init__(self, manager):
        self.manager = manager
        self._middlewares = Middleware()


class Manager:
    def __init__(self, storage, default_locale):
        self.storage = storage
        self.default_locale = default_locale
    
    def get_window(self, *args, **kwargs):
        return FakeRawWindow
    
    async def close(self):
        pass

FakeLoader = Loader()
FakeStorage = Storage()
FakeManager = Manager(FakeStorage, 'en')


def with_workdir(path: str) -> str:
    return os.path.join(WORK_DIR, path)
