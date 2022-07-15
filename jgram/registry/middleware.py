import inspect
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from aiogram.dispatcher.handler import _check_spec, _get_spec


@dataclass
class MiddlewareObj:
    middleware: Callable
    spec: inspect.FullArgSpec

    async def call(self, args: Tuple, kwargs: Dict):
        return await self.middleware(*args, **_check_spec(self.spec, kwargs))


class ProcessMiddleware:
    """
    Middlewares manager
    """
    def __init__(self):
        self._middlewares: List[MiddlewareObj] = []
        self._named_middlewares: Dict[str, MiddlewareObj] = {}
        
        
    def register(self, middleware: Callable, name: Optional[str] = None):
        """
        Register callback as middleware

        :param middleware: callback that be registered
        :param name: the name of the window for which will be called middleware, defaults to None
        :return:
        """
        middleware = MiddlewareObj(
            middleware=middleware,
            spec=_get_spec(middleware)
        )
        if name is not None:
            self._named_middlewares[name] = middleware
        else:
            self._middlewares.append(middleware)
        
    async def process(self, name: Optional[str] = None, *args, **kwargs) -> bool:
        """
        call middleware
        
        :param name: name of the window for which will be called middleware, defaults to None
        :return: flag that tells whether to continue rendering or not
        :rtype: bool
        """
        if name is not None and name in self._named_middlewares:
            result = await self._named_middlewares[name].call(args, kwargs)
            if result is False:
                return False
        else:
            for middleware in self._middlewares:
                result = await middleware.call(args, kwargs)
                if result is False:
                    return False
        return True
