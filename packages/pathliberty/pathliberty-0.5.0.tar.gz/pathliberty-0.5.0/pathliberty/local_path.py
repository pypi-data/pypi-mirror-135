from __future__ import annotations
import os
from pathlib import _NormalAccessor
from pathliberty.base import AbstractPath, AbstractPathAccessor

class NormalAccessor(_NormalAccessor, AbstractPathAccessor):
    chown = os.chown

class LocalPath(AbstractPath):
    __slots__ = ()
    accessor_class = NormalAccessor

    def new(self, path: AbstractPath) -> LocalPath:
        return LocalPath(path)
