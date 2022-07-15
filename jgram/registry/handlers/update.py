
from typing import TYPE_CHECKING, Union

from aiogram.types import CallbackQuery, Message

from jgram.context import Context
from jgram.loggers import handler_logger
from jgram.storage.protocols import StorageRecord
from jgram.window.window import ShowMode

if TYPE_CHECKING:
    from ..registry import Registry


async def update_handler(update: Union[CallbackQuery, Message], 
                         registry: 'Registry', 
                         window_name: str, 
                         user: StorageRecord,
                         build_next_step: bool = True):
    manager = registry.manager
    kwargs = {
        'manager': manager
    }
    
    locale = user.locale
    if locale is None:
        locale = manager.default_locale
    
    if isinstance(update, CallbackQuery):
        window_name = update.data
        mode = ShowMode.EDIT
        raw_window = manager.get_window(window_name, locale)
        handler_logger.debug(
            "update type is CallbackQuery "
            "start rendering window using CallbackQuery.data "
            "as window name"
        )
        
    else:
        mode = ShowMode.SEND
        raw_window = manager.get_window(name=window_name, 
                                        locale=locale)
        
        filter_passed = False
        
        if raw_window.filters:
            for filters in raw_window.filters:

                next_step, filters = registry.filters_factory.build(
                    filters=filters,
                    handler=registry.dispatcher.message_handlers
                )
                checked = await registry.filters_factory.check(
                    filters,
                    update
                )
                if checked is not False:
                    kwargs.update(checked)
                    filter_passed = True
                    raw_window = manager.get_window(name=next_step, 
                                                    locale=locale)
                    break

        if (
            filter_passed is False and
            build_next_step
            ):
                if raw_window.next_step:
                    window_name = raw_window.next_step
                    raw_window = manager.get_window(name=window_name, locale=locale)
                else:
                    await manager.storage.reset_data(user_id=update.from_user.id)
                    return
            
        if (
            raw_window.allowed_updates and
            update.content_type not in 
            raw_window.allowed_updates
        ):
            handler_logger.debug(
                f"content type {update.content_type!r} not passed to "
                f"allowed updates {raw_window.allowed_updates}, skip window update"
            )
            return

    context = Context(
        user_id=update.from_user.id,
        locale=locale,
        data=user.data,
        window_name=raw_window.window_name
    )
    kwargs['context'] = context

    if (
        (await registry.middlewares.process(
            None, update, **kwargs)) is False
        or (await registry.middlewares.process(
            context.window_name, update, **kwargs)) is False
        ):
        
        return

    if not context.window_name:
        return
    
    if context.window_name != raw_window.window_name:
        raw_window = manager.get_window(name=context.window_name, 
                                        locale=context.locale)

    await manager.update_window(
        update=update,
        locale=context.locale,
        context_data=context.data,
        mode=mode,
        raw_window=raw_window
    )
    
    if raw_window.reset_context:
        handler_logger.debug(
            "'reset_context' field is True "
            "reset user context"
        )
        context.reset()

    await manager.storage.update_data(
        user_id=update.from_user.id,
        data=context.data)
