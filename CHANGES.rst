Jgram 1.0.0-alpha (2022-06-28)
==============================

Features
--------

- Added named middlewares

  for example

  .. code-block:: python

    
    async def middleware(update, manager, context):
      pass

    async def named_middleware(update, manager, context):
      pass

    async def main():
      registry = Registry(token='')
      registry.register_middleware(middleware) # works for all windows
      registry.register_middleware(named_middleware, name='window_name') # works for window with name 'window_name'

- Added middleware decorator
  
  for example

  .. code-block:: python

    registry = Registry(token='')

    @registry.middleware(name='window_name')
    async def middleware(update, manager, context):
      pass

- Added .reset method to :code:`jgram.context.Context`, it will clear data and set window_name to None
- added start_window attribute to :code:`manager.windows_manager.WindowsManager`, for change standart window rendered for /start command
  
  for example

  .. code-block:: python

    manager = WindowsManager(start_window='another_window') # by default renders window with name 'start'

Misc
--------

- renamed:
  
  :code:`jgram.text` -> :code:`jgram.window`

  :code:`jgram.text.RawText` -> :code:`jgram.window.RawWindow`

  :code:`jgram.text.Text` -> :code:`jgram.window.Window`

  :code:`jgram.manager.texts_manager` -> :code:`jgram.manager.windows_manager`

  :code:`jgram.manager.windows_manager.TextsManager` -> :code:`jgram.manager.windows_manager.WindowsManager`
  
  :code:`jgram.manager.windows_manager.WindowsManager.load_texts` -> :code:`jgram.manager.windows_manager.WindowsManager.load_windows`
  
  :code:`jgram.manager.windows_manager.WindowsManager.get_text` -> :code:`jgram.manager.windows_manager.WindowsManager.get_window`
  
  :code:`jgram.manager.windows_manager.WindowsManager.update_text` -> :code:`jgram.manager.windows_manager.WindowsManager.update_window`
  
  :code:`jgram.manager.windows_manager.WindowsManager.show_text` -> :code:`jgram.manager.windows_manager.WindowsManager.show_window`
  
  :code:`jgram.manager.windows_manager.WindowsManager.send_text` -> :code:`jgram.manager.windows_manager.WindowsManager.send_window`
  
  :code:`jgram.manager.windows_manager.WindowsManager.edit_text` -> :code:`jgram.manager.windows_manager.WindowsManager.edit_window`
  
  :code:`jgram.storage.protocols.BaseStorage.update_locale` -> :code:`jgram.storage.protocols.BaseStorage.set_locale`

  exceptions:
    :code:`jgram.exceptions.TextNotFoundError` -> :code:`jgram.exceptions.WindowNotFoundError`

- ! rewriten update handle logic, :code:`jgram.registry.event_checker` removed, update handling provided by :code:`jgram.registry.handlers.update.update_handler`
- added :code:`.wait_closed` method to storage
- moved:

  :code:`jgram.window.media` -> :code:`jgram.window.media.media`

  :code:`jgram.window.markup` -> :code:`jgram.window.markup.markup`

  :code:`jgram.window.tools` -> :code:`jgram.window.markup.tools`

- include registry and check current user window logic moved to :code:`jgram.registry.filters` and use :code:`aiogram.dispatcher.filters.Filter`
