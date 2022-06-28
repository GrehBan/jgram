import pytest

from jgram.storage.memory import MemoryStorage

from . import FakeStorage, FakeUser


class TestStorage:
    storage = MemoryStorage()
    _USER_KEYS_ = [
        'data',
        'locale',
        'window_name'
    ]
    
    @pytest.mark.asyncio
    async def test_storage_data_structure(self):
        created = await self.storage.create_user(user_id=FakeUser.id)
        
        assert isinstance(created, dict) \
            and len(created) == len(self._USER_KEYS_) and\
            all((key in self._USER_KEYS_ for key in created))
    
    @pytest.mark.asyncio
    async def test_storage_data_update_get(self):
        try:
            await self.storage.update_data(user_id=FakeUser.id, 
                                           create_user=False,
                                           data=FakeStorage._user_data)
            assert (await self.storage.get_data(user_id=FakeUser.id))\
                == FakeStorage._user_data
        except (KeyError, ValueError):
            assert False
    
    @pytest.mark.asyncio
    async def test_storage_locale_set_get(self):
        try:
            await self.storage.set_locale(user_id=FakeUser.id,
                                                  create_user=True,
                                                  locale='en')
            assert (await self.storage.get_locale(user_id=FakeUser.id))\
                == 'en'
        except (KeyError, ValueError):
            assert False

    @pytest.mark.asyncio
    async def test_storage_delete(self):
        try:
            await self.storage.reset_data(user_id=FakeUser.id,
                                          create_user=True)
            assert (await self.storage.get_data(user_id=FakeUser.id))\
                == {"window_name": None}
        except (KeyError, ValueError):
            assert False

        await self.storage.delete_user(user_id=FakeUser.id)
        with pytest.raises(ValueError):
            await self.storage.get_user(user_id=FakeUser.id)
