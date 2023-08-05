from __future__ import annotations
import abc
from pathlib import PosixPath
from typing import Any, Callable

from pathliberty.base import AbstractPath

class AbstractRemotePath(AbstractPath):
    """ Represents a path that exists on a some remote node """
    __slots__ = ()

    @abc.abstractmethod
    def cwd(self): raise NotImplementedError

    @abc.abstractmethod
    def home(self): raise NotImplementedError

    # @abc.abstractmethod
    # def glob(*args): raise NotImplementedError

    # @abc.abstractmethod
    # def rglob(*args): raise NotImplementedError

    @abc.abstractmethod
    def open(*args): raise NotImplementedError

    @abc.abstractmethod
    def touch(*args): raise NotImplementedError

    @abc.abstractmethod
    def is_equal_to(self, other) -> bool:
        raise NotImplementedError

    def _rich_comparison(self, method: Callable, other: Any) -> bool:
        if isinstance(other, AbstractRemotePath):
            if not self.is_equal_to(other):
                return NotImplemented
        return method(other)

    def __eq__(self, other): return self._rich_comparison(super().__eq__, other)
    def __lt__(self, other): return self._rich_comparison(super().__lt__, other)
    def __le__(self, other): return self._rich_comparison(super().__le__, other)
    def __gt__(self, other): return self._rich_comparison(super().__gt__, other)
    def __ge__(self, other): return self._rich_comparison(super().__ge__, other)
    __hash__ = PosixPath.__hash__
