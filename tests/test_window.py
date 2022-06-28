import pytest

from jgram.exceptions import InvalidWindowFieldsMap
from jgram.window import RawWindow


class TestWindow:
    
    def test_valid_window(self):
        window = RawWindow(
            window_name='start',
            text='text',
            media=None,
            parse_mode='HTML',
            web_preview=True,
            markup=None
        )
        try:
            window.build({})
        except InvalidWindowFieldsMap:
            assert False

    def test_window_invalid(self):
        with pytest.raises(InvalidWindowFieldsMap):
            RawWindow(window_name='start').build({})
    
    def test_window_invalid_markup(self):
        with pytest.raises(InvalidWindowFieldsMap):
            RawWindow(
                window_name='start',
                markup={
                    "type": "unknown"
                }
                ).build({})
            
    def test_window_invalid_markup_button(self):
        with pytest.raises(InvalidWindowFieldsMap):
            RawWindow(
                window_name='start',
                markup={
                    "type": "inline",
                    "markup": [[
                        {
                            "unknown_key": "unknown_value"
                        }
                    ]]
                }
            ).build({})
        