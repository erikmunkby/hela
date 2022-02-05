from pathlib import Path
from typing import Union


def join_paths(*paths: Union[str, Path]) -> Path:
    return Path('/'.join([split for p in paths for split in str(p).split('/')]))
