import os
import os.path
from typing import Tuple

from .. import _types


def abspath(fp: _types.PathLike) -> _types.PathLike:
    return os.path.abspath(fp)


def joinpath(path: _types.PathLike, *paths: Tuple[_types.PathLike]) -> _types.PathLike:
    return abspath(os.path.join(path, *paths))


def iterdir(dp: _types.PathLike) -> _types.PathLike:
    for fp in os.listdir(dp):
        yield joinpath(dp, fp)

