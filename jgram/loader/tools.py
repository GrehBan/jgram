import os
import os.path
from typing import Tuple, Union


def abspath(fp: str) -> str:
    return os.path.abspath(fp)


def joinpath(path: str, *paths: Tuple[str]) -> str:
    return abspath(os.path.join(path, *paths))


def iterdir(dp: str) -> str:
    for fp in os.listdir(dp):
        yield joinpath(dp, fp)

