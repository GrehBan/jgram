# JGram

## About the project
Jgram was created to be able to quickly and conveniently write telegram bots, placing their structure in .json files
Jgram based on [AIOgram-2.21](https://github.com/aiogram/aiogram/tree/v2.21) framework

for development info see [TODO](/TODO.md) and [CHANGES](/CHANGES.rst)

## Table of contents
- [Installation](#installation)
    - [From sources](#from-sources)
    - [From PYPI](#from-pypi)
- [Getting started](#getting-started)
- [Initialization](#initialization)
    - [Registry](#registry)
    - [Windows manager](#windows-manager)
    - [Storage](#storage)
    - [Loader](#loader)
- [Windows](#windows)
    - [Fields](#fields)
    - [Loading windows](#loading-windows)
- [Middlewares](#middlewares)
- [Filters](#filters)
    - [Aioram's filters](#aiograms-filters)
    - [Middleware as filter](#middleware-as-filter)

## installation

### From sources

```bash
git clone https://github.com/GrehBan/jgram.git
cd jgram
poetry install --no-dev
```

### From PYPI

```bash
pip install jgram
```

### Speedups
```bash
pip install uvloop cchardet aiodns ujson
```

or 

```bash
pip install jgram[fast]
```

## Getting started

windows.json

```json
{
    "locale": "en",
    "start": {
        "text": "Hello unknown user",
        "markup": {
            "type": "inline",
            "markup": [
                [
                    {
                        "text": "Register",
                        "callback_data": "write_name"
                    }
                ]
            ]
        }
    },
    "write_name": {
        "text": "Write your name please",
        "markup": {
            "type": "inline",
            "markup": [
                [
                    {
                        "text": "back",
                        "callback_data": "start"
                    }
                ]
            ]
        },
        "next_step": "write_age"
    },
    "write_age": {
        "text": "Your name is {name}\nwrite your age please",
        "markup": {
            "type": "inline",
            "markup": [
                [
                    {
                        "text": "back",
                        "callback_data": "write_name"
                    }
                ]
            ]
        },
        "allowed_updates": ["text"],
        "next_step": "save_data"

    },
    "save_data": {
        "text": "Your name is {name}\nYou {age} years old\nThank you!",
        "allowed_updates": ["text"]
    }
}

```

[simple.py](/examples/simple.py)

```python
import asyncio
import os

from jgram import Registry
from jgram.context import Context
from jgram.manager import WindowsManager


async def name_formatter(update, manager: WindowsManager, context: Context):
    context.data['name'] = update.text


async def age_formatter(update, manager: WindowsManager, context: Context):
    context.data['age'] = update.text


async def main():
    registry = Registry(token=os.getenv('BOT_TOKEN'))
    registry.manager.load_windows('windows.json')
    registry.register_middleware(name_formatter, name='write_age')
    registry.register_middleware(age_formatter, name='save_data')

    try:
        await registry.start()
    finally:
        await registry.close()


if __name__ == '__main__':
    asyncio.run(main())
```

## Initialization
 
 ### Registry
 ```python
 from jgram import Registry

 registry = Registry()

 # initialization arguments

    # registry initialize bot and dispatcher from one of this arguments, and must have one of it

    bot -> typing.Optional[aiogram.Bot] # current aiogram's bot

    dispatcher -> typing.Optional[aiogram.Dispatcher] # current aiogram's dispatcher

    token -> typing.Optional[str] # bot's token


    # registry initialize new jgram.WindowsManager instance, if manager argument is not provided
    manager -> typing.Optional[jgram.WindowsManager] # current manager for manage windows
 ```

### Windows manager
```python
from jgram import WindowsManager

manager = WindowsManager()

# initialization arguments

    # manager initialize new jgram.loader.JsonLoader instance, if loader arguemnt is not provided
    loader -> typing.Optional[jgram.loader.protocols.LoaderProto] # current loader for load raw json

    # manager initialize new jgram.storage.memory.MemoryStorage, if storage argument is not provided
    storage -> typing.Optional[jgram.storage.protocols.BaseStorage] # current users data storage

    start_window -> str # name of window than be rendered when /start command is handled
        default = "start"
```

## Storage
```python
from jgram.storage.memory import MemoryStorage # memory storage for example

storage = MemoryStorage()
```

## Loader
```python
from jgram.loader import JsonLoader

loader = JsonLoader()

# initialization arguments

    default_locale -> typing.Optional[str] # locale which will be used if "locale" field in window is not provided, if set to None, all of windows must have "locale" field
        default = 'en'
    json_loads -> typing.Callable[..., Any] # function to loads json from string
        default = json.loads # python's built-in json's module func
```

## Windows

### Structure

```json
{
  "lang": "{lang}",
  "{text_name}": {
    "text": "{text}",
    "media": {
        "type": "{media_type}",
        "url": "{media_url}",
        "path": "{media_path}",
        "file_id": "{media_file_id}"
    }
    "markup": {
        "type": "{type}",
        "markup":
        [
            [{"text": "Button text", "callback_data": "{next_step callback data}"}],
            [{"text": "Url button", "url": "{url}"}],
            [{"text": "Reply button"}]
        ],
    "parse_mode": null,
    "web_preview": false,
    "allowed_updates": ["{update_type}"],
    "filters": [
        {
            "{filter_name}": "{value}",
            "next_step": "{value}"
        }
    ],
    "next_step": "{value}",
    "reset_context": false
  }
}
}
```

### Fields

```python 
"lang" -> typing.Optional[str] # Locale of windows
```

```python
"text" -> typing.Optional[str] # bot message text, uses as a caption to media, if it set
```

```python
"media" -> typing.Optional[typing.Dict] # bot message media
    "type" -> str # media type
        values = ["photo", "video", "animation", "audio", "document"]
    
    # media must have one of this fields

    "url" -> typing.Optional[str] # media url
    
    "path" -> typing.Optional[str] # path to media file

    "file_id" -> typing.Optional[str] # media file id
```

```python
"markup" -> typing.Optional[typing.Dict] # bot message reply markup
    "type" -> str # markup type
        values = ["inline", "reply"]
    
    "markup" typing.List[typing.List[typing.Dict[str, str]]] # list of lists of markup buttons
```

```python
"parse_mode" -> typing.Optional[str] # bot message parse mode
    values = ["HTML", "MARKDOWN", "MARKDOWN_V2"]
```

```python
"web_preview" -> bool # bot message disable or enable web preview
    default = False
```

```python
"allowed_updates" -> typing.List[str] # list of content types allowed for processing
    default = []
    values = ["text", "photo", "video", "animation", "audio", "document"]
```

```python
"filters" -> typing.List[typing.Dict] # list of dicts than represents aiogram's filters
    default = []

    "{filter_name}" -> str # Aiogram's filter value
    ...
    "next_step" -> str # name of window than be rendered when filters passed
```

```python
"next_step" -> typing.Optional[str] # name of window than be rendered if any filter not passed or filters not found
```

```python
"reset_context" -> bool # reset current user context
    default = False
```

### Loading windows

```python
from jgram import WindowsManager

manager = WindowsManager()
manager.load_windows("path/to/file/windows.json")
```

## Middlewares

middlewares call before window rendered, and in middleware you can change user context data or manipulate window processing

middlewares can return a True or False, if returns True, update handler will continue render window, but if returns False, window will not be rendered

for example

```python
from aiogram.types import Message, CallbackQuery

from jgram import Registry
from jgram.context import Context
from jgram.manager import WindowsManager


async def middleware(
    update: typing.Union[Message, CallbackQuery],
    manager: WindowsManager, 
    context: Context
    ):
    if isinstance(update, CallbackQuery):
        return True # skip middleware processing, and render window
    context.data['name'] = update.text # save current message text to "name" field


registry = Registry()
registry.register_middleware(middleware) # middleware will be processed for all windows

# if you can process middleware only for one window
registry.register_middleware(middleware, name="window_name")
```

## Filters

you have two ways to filter update

### Aiogram's filters

you can use aiogram's filters, to filter update, but only if filter have key field

for example

```json
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
```

if current update chat id is 123 renders "chat_123" window, in another situations renders "any_another_chat" window

## Middleware as filter

you can use jgram's middleware as filter

for example

```python
from aiogram.types import Message, CallbackQuery

from jgram.context import Context
from jgram.manager import WindowsManager


async def middleware(
    update: typing.Union[Message, CallbackQuery],
    manager: WindowsManager, 
    context: Context
    ):
    if isinstance(update, CallbackQuery):
        return True # skip middleware processing, and render window
    try:
        age = int(update.text) # try to convert text to age int
    except ValueError:
        return False # skip window rendering
        # context.window_name = "error_window" # or switch window
```
