import pytest

from jgram.storage.memory import MemoryStorage
from jgram.storage.protocols import StorageRecord

from . import FakeStorage, FakeUser


class TestStorage:
    storage = MemoryStorage()
    @pytest.mark.asyncio
    async def test_storage_data_structure(self):
        record = await self.storage.get_user(user_id=FakeUser.id)
        
        assert isinstance(record, StorageRecord)\
            and record.window_name is None and\
                record.locale is None and\
                record.data == {}
                    
    @pytest.mark.asyncio
    async def test_storage_data_update_get(self):
        try:
            await self.storage.update_data(user_id=FakeUser.id, 
                                           data=FakeStorage._user.data)
            assert (await self.storage.get_data(user_id=FakeUser.id))\
                == FakeStorage._user.data
        except (KeyError, ValueError):
            assert False
    
    @pytest.mark.asyncio
    async def test_storage_locale_set_get(self):
        try:
            await self.storage.set_locale(user_id=FakeUser.id,
                                                  locale='en')
            assert (await self.storage.get_locale(user_id=FakeUser.id))\
                == 'en'
        except (KeyError, ValueError):
            assert False

    @pytest.mark.asyncio
    async def test_storage_delete_data(self):
        try:
            await self.storage.reset_data(user_id=FakeUser.id)
            assert (await self.storage.get_data(user_id=FakeUser.id))\
                == {}
        except (KeyError, ValueError):
            assert False
