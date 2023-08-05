from __future__ import annotations

import abc
from pathlib import PosixPath
from typing import Optional, Sequence, TypeVar, Union
from datetime import datetime as datetime

_PT = TypeVar('_PT')

class AbstractPathAccessor:
    def __init__(self, path_obj: AbstractPath) -> None:
        pass

    @staticmethod
    def raise_not_implemented(*args, **kwargs):
        raise NotImplementedError

    stat = raise_not_implemented
    lstat = raise_not_implemented
    open = raise_not_implemented
    listdir = raise_not_implemented
    scandir = raise_not_implemented
    chmod = raise_not_implemented
    chown = raise_not_implemented
    lchmod = raise_not_implemented
    mkdir = raise_not_implemented
    unlink = raise_not_implemented
    link_to = raise_not_implemented
    rmdir = raise_not_implemented
    rename = raise_not_implemented
    replace = raise_not_implemented
    symlink = raise_not_implemented
    utime = raise_not_implemented
    readlink = raise_not_implemented


class AbstractPath(PosixPath, metaclass=abc.ABCMeta):
    """ An abstract class that overrides pathlib.PurePath and pathlib.Path
    methods to implement casting to the AbstractPath subclass

    """
    __slots__ = ()

    accessor_class = AbstractPathAccessor

    def __init__(self, *args, **kwargs) -> None:
        self._accessor = self.accessor_class(self)

    @abc.abstractmethod
    def new(self, path: _PT) -> AbstractPath:
        """ Return a new instance of AbstractPath

        It is useful for path initialized via object.__new__(cls) by PurePath (i.e. PurePath._from_parts).
        Inside this method we can initialize attributes that cannot be initialized because of PurePath initializing logic
        """
        raise NotImplementedError

    # below are overridden pathlib.PurePath methods
    def __truediv__(self, key) -> AbstractPath:
        return self.new(super().__truediv__(key))

    def __rtruediv__(self, key) -> AbstractPath:
        return self.new(super().__truediv__(key))

    def with_name(self, name) -> AbstractPath:
        return self.new(super().with_name(name))

    def with_suffix(self, suffix) -> AbstractPath:
        return self.new(super().with_suffix(suffix))

    def relative_to(self, *other) -> AbstractPath:
        return self.new(super().relative_to(other))

    def joinpath(self, *args) -> AbstractPath:
        return self.new(super().joinpath(args))

    @property
    def parent(self) -> AbstractPath:
        return self.new(super().parent)

    @property
    def parents(self) -> Sequence[AbstractPath]:
        return [self.new(parent) for parent in super().parents]

    # below are overridden pathlib.Path methods
    def _make_child_relpath(self, part) -> AbstractPath:
        return self.new(super()._make_child_relpath(part))

    def absolute(self) -> AbstractPath:
        return self.new(super().absolute())

    def resolve(self, strict=False) -> AbstractPath:
        return self.new(super().resolve(strict))

    def rename(self, target) -> AbstractPath:
        return self.new(super().rename(target))

    def replace(self, target) -> AbstractPath:
        return self.new(super().replace(target))

    def expanduser(self) -> AbstractPath:
        return self.new(super().expanduser())

    def getsize(self):
        """Return the size of a file, reported by self.stat()."""
        return self.stat().st_size

    def getmtime(self, dt: bool = False) -> Union[float, datetime]:
        """Return the last modification time of a file, reported by self.stat()."""
        timestamp = self.stat().st_mtime
        if dt:
            return datetime.fromtimestamp(timestamp)
        else:
            return timestamp

    def getatime(self, dt: bool = False) -> Union[float, datetime]:
        """Return the last access time of a file, reported by self.stat()."""
        timestamp = self.stat().st_atime
        if dt:
            return datetime.fromtimestamp(timestamp)
        else:
            return timestamp

    def chown(self, uid: Optional[int] = None, gid: Optional[int] = None):
        """
        Change the owner (``uid``) and group (``gid``) of a file.
        """
        uid = uid or self.stat().st_uid
        gid = gid or self.stat().st_gid
        self._accessor.chown(self, uid, gid)
