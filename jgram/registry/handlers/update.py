
from typing import TYPE_CHECKING, Dict, Union

from aiogram.types import CallbackQuery, Message

from jgram.context import Context
from jgram.loggers import handler_logger
from jgram.window.window import ShowMode

if TYPE_CHECKING:
    from ..registry import Registry


async def update_handler(update: Union[CallbackQuery, Message], 
                         registry: 'Registry', 
                         window_name: str, 
                         user: Dict,
                         build_next_step: bool = True):
    manager = registry.manager
    locale = user['locale']
    if locale is None:
        locale = manager.default_locale
    
    # get raw window
    if isinstance(update, CallbackQuery):
        # if update is inline button click build window from callback_query.data
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
        raw_window = manager.get_window(name=window_name, locale=locale)
        filter_passed = False
        if raw_window.input_filters: # filter input
            for filter in raw_window.input_filters:
                if filter['text'] == update.text: # check all filters if pass to input
                    raw_window = manager.get_window(name=filter['next_step'], 
                                                    locale=locale)
                    filter_passed = True
                    break
        if (
            filter_passed is False and
            build_next_step and
            raw_window.next_step
            ): # if filters not passed and need render next step, get it
            window_name = raw_window.next_step
            raw_window = manager.get_window(name=window_name, locale=locale)
        elif not raw_window.next_step and build_next_step:
            await manager.storage.reset_data(user_id=update.from_user.id,
                                             create_user=True)
            return
            
        # check allowed updates
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
    
    user['data']['window_name'] = raw_window.window_name
    context = Context(
        user_id=update.from_user.id,
        locale=locale,
        data=user['data'],
        window_name=raw_window.window_name
    ) # build context

    # process middlewares
    # if any middleware returns False, update processing was stop
    if (
        (await registry._middlewares.process(
            None, update, manager, context)) is False
        or (await registry._middlewares.process(
            window_name, update,manager, context)) is False
        ):
        
        return
    
    await manager.update_window(
        update=update,
        locale=context.locale,
        context_data=context.data,
        mode=mode,
        raw_window=raw_window
    ) # update window name in storage, and render window
    
    # reset context if need
    if raw_window.reset_context:
        handler_logger.debug(
            "'reset_context' field is True "
            "reset user context"
        )
        context.reset()

    # save context data to storage
    await manager.storage.update_data(
        user_id=update.from_user.id,
        create_user=True,
        data=context.data)
