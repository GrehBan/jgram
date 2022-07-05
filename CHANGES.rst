Jgram 1.0.4-alpha (2022-07-05)
==============================

Features
--------
- Added support of custom loads functions in loader, you can pass your function in initialization arguments
  
  for example

  .. code-block:: python

    
    import ujson
    from jgram.loader import JsonLoader
    
    loader = JsonLoader(json_loads=ujson.loads)

Bugfix
--------
- Fixed bug with stop check aiogram's filters, if one not passed
- Fixed bug with no change window, if it changed in context

Misc
--------
- Removed :code:`.delete_user` :code:`.check_user` :code:`.create_user` methods from storage
- Created :code:`jgram.storage.protocols.StorageRecord` record, that represents a user record in storage
- :code:`jgram.storage.memory.MemoryStorage` start using :code:`collections.defaultdict` as storage
- Removed :code:`jgram.json` module, use :code:`json_loads` attribute in loaders instead
- Renamed loaders :code:`.load_json` method to :code:`.load_windows`
- Renamed :code:`jgram.registry.filters` to :code:`jgram.registry.includer`
- From :code:`jgram.registry.includer` deleted :code:`HaveWindow` and :code:`IncludeRegistry` filters, created :code:`IncludeData` instead
- Clean

Jgram 1.0.2-alpha (2022-06-28)
==============================

Features
--------
- Added full support of aiogram's filters
  
  for example

  .. code-block:: javascript

    {
      "filtered": {
        "text": "Hello",
        "filters": [
          {
          "chat_id": 123,
          "next_step": "chat_123"
          }
        ],
        "next_step": "any_another_chat"
      }
    }
  
  if current update chat id is 123 renders "chat_123" window, in another situations renders "any_another_chat" window

Misc
--------
- Moved users data :code:`user["data"]["window_name"]` field to :code:`user["window_name"]`
- added :code:`.set_window` and :code:`.get_window` methods to storage
- method :code:`.load_user` moved from :code:`jgram.storage.protocols.BaseStorage` to :code:`jgram.storage.protocols.StorageProto` and marked as abtract method
- renamed :code:`input_filters` window field to :code:`filters`

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
- added start_window attribute to :code:`jgram.manager.windows_manager.WindowsManager`, for change standart window rendered for /start command
  
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
