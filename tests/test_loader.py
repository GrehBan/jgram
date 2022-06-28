import pytest

from jgram.exceptions import InvalidFileType, InvalidJsonFormat, InvalidProcessedFormat
from jgram.loader import JsonLoader

from . import with_workdir


class TestLoader:
    loader = JsonLoader()
    
    def test_loader_valid_data(self):
        
        try:
            self.loader.load_json(with_workdir('windows/valid.json'))
        except (InvalidFileType, InvalidJsonFormat, InvalidProcessedFormat):
            assert False

    def test_loader_invalid_data(self):
        with pytest.raises((InvalidJsonFormat, InvalidProcessedFormat)):
            self.loader.load_json(with_workdir('windows/invalid.json'))
            
    def test_loader_not_json(self):
        with pytest.raises(InvalidFileType):
            self.loader.load_json(with_workdir('windows/not_json'))

    def test_unset_locale(self):
        self.loader._default_locale = None
        
        with pytest.raises(InvalidProcessedFormat):
            self.loader.load_json(with_workdir('windows/valid_without_locale.json'))
