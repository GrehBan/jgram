import pytest

from jgram.registry import Registry

from . import FakeBot, FakeManager


class TestRegistry:
    registry = Registry(bot=FakeBot, manager=FakeManager)
    
    @pytest.mark.asyncio
    async def test_registry_closed(self):

        await self.registry.close()
        assert FakeBot._session is None or \
            FakeBot._session.closed
