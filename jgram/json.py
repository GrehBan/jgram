from typing import IO, AnyStr, Dict, List, Union

try:
    import ujson as json  # type: ignore
    
    DecodeError = json.JSONDecodeError
    

except ImportError:
    import json
    
    DecodeError = json.decoder.JSONDecodeError

AvailableJsonValues = Union[str, int, float, list, dict]
JsonValueType = Union[List['JsonValueType'], AvailableJsonValues, 'LoadedJson']
LoadedJson = Dict[str, JsonValueType]


def load(fp: IO[AnyStr]) -> LoadedJson:
    return json.load(fp)


def loads(s: AnyStr) -> LoadedJson:
    return json.loads(s)


def dump(obj: LoadedJson, fp: IO[AnyStr]) -> None:
    return json.dump(obj, fp, ensure_ascii=False)


def dumps(obj: LoadedJson) -> str:
    return json.dumps(obj, ensure_ascii=False)
