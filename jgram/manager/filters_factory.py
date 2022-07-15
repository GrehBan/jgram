from typing import Dict, Tuple

from aiogram import Dispatcher
from aiogram.dispatcher.filters import FilterNotPassed, check_filters, get_filters_spec
from aiogram.dispatcher.handler import Handler

from .protocols import FiltersFactoryProto, FiltersList


class FiltersFactory(FiltersFactoryProto):
    def __init__(self,
                 dispatcher: Dispatcher):
        self._dispatcher = dispatcher

    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher
    
    def build(self, filters: Dict, handler: Handler) -> Tuple[str, FiltersList]:
        filters = filters.copy()
        next_step = filters.pop('next_step')
        
        return next_step, \
            self.dispatcher.filters_factory.resolve(
                event_handler=handler,
                **filters
            )

    async def check(self, filters_list: FiltersList, *args):
        try:
            return await check_filters(
                filters=get_filters_spec(self.dispatcher, filters_list),
                args=args
            )
        except FilterNotPassed:
            return False
