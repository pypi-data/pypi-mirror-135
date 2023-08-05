from __future__ import annotations
from os import path

import paramiko
from typing import ContextManager, Dict, Iterable, Optional, Tuple, Union
from pathliberty import AbstractPathAccessor
from pathliberty import AbstractRemotePath
from pathliberty.ssh import SSHSession


class SSHAccessor(AbstractPathAccessor):
    """ Class for manipulating remote files over SSH """

    _ssh_clients: Dict[Tuple, paramiko.SSHClient] = {}

    #TODO: shared client object for same host, proxy
    # def __init__(self, path_obj: SSHPath) -> None:
    def __init__(self, path_obj: SSHPath) -> None:
        # self.host = path_obj.host
        # self.proxy = path_obj.proxy


        # if client := self._ssh_clients.get(self.client_key):
        #     self.ssh = client
        # else:
        #     self.ssh = get_ssh(
        #             self.host,
        #             jump_host=self.proxy,
        #         )
        #     self._ssh_clients[self.client_key] = self.ssh

        # self._sftp_open = False

        # self.client = path_obj.ssh.client
        self.sftp = path_obj.ssh.sftp


    # @property
    # def client_key(self):
    #     return (self.host, self.proxy)

    # @property
    # def sftp(self) -> paramiko.SFTPClient:
    #     if not self._sftp_open:
    #         try:
    #             self._sftp = self.ssh.open_sftp()
    #             self._sftp_open = True
    #         except Exception:
    #             self._sftp = None

    #     return self._sftp

    # def is_connected(self):
    #     return self.ssh.get_transport() is not None

    # def __del__(self):
    #     # if self.is_connected():
    #     #     if self.sftp:
    #     #         self.sftp.close()
    #     #     if self.ssh:
    #     #         self.ssh.close()
    #     print(f"\ndelete accessor {self}: {self._ssh_clients = }")
    #     # del self._ssh_clients[self.client_key]


    def stat(self, path):
        return self.sftp.stat(str(path))

    def lstat(self, path):
        return self.sftp.lstat(str(path))

    def listdir(self, path):
        return self.sftp.listdir(str(path))

    def scandir(self, path: SSHPath) -> ContextManager[Iterable[SSHPath]]:
        class _ScandirIterator:
            """ A temporary iterator to support the following pathlib constructions:
                with scandir(parent_path) as scandir_it:
                    entries = list(scandir_it)

            Objects of this class are intended to be used instead of os.DirEntry objects inside pathlib._Selector's
            """
            def __init__(this, path: SSHPath): this.path = path
            def __enter__(this): return this
            def __exit__(*args): pass
            def __iter__(this):
                new_path = this.path.new
                for p in self.listdir(path):
                    yield this.path / new_path(p)

        return _ScandirIterator(path)

    def chmod(self, mode):
        self.sftp.chmod(self(str), mode)

    def mkdir(self, path, mode=0o777):
        self.sftp.mkdir(str(path), mode=mode)

    def remove(self, path):
        self.sftp.remove(str(path))

    unlink = remove

    def rmdir(self, path: SSHPath):
        self.sftp.rmdir(str(path))

    def rename(self, src: SSHPath, dst):
        self.sftp.rename(str(src), dst)

    def rename(self, src: SSHPath, dst):
        self.unlink(dst)
        self.rename(src, dst)

    def symlink(self, target, source):
        self.sftp.symlink(str(source), target)

    def utime(self, path, times):
        self.sftp.utime(str(path), times)

    def readlink(self, path):
        return self.sftp.readlink(str(path))

    def chown(self, path, uid, gid):
        self.sftp.chown(str(path), uid, gid)


class SSHPath(AbstractRemotePath):
    __slots__ = ('host', 'proxy', 'ssh')
    accessor_class = SSHAccessor

    def __init__(
        self,
        *pathsegments,
        host: Optional[str] = None,
        proxy: Optional[str] = None,
        ssh: Optional[SSHSession] = None,
    ):

        if host and ssh:
            raise RuntimeError("host and ssh arguments cannot be specified together")

        if not ssh and not host:
            raise RuntimeError("at least one of the host or ssh arguments must be specified")

        if not ssh:
            self.ssh = SSHSession(
                host,
                jump_host=proxy,
            )
        else:
            self.ssh = ssh

        self.host = self.ssh.host
        self.proxy = self.ssh.proxy

        super().__init__(pathsegments)

    def is_equal_to(self, other) -> bool:
        if (self.ssh.host, self.ssh.proxy) == (other.ssh.host, other.ssh.proxy):
            return True

    @property
    def sftp(self) -> paramiko.SFTPClient:
        return self.ssh.sftp

    def new(self, path: Union[str, AbstractRemotePath]) -> SSHPath:
        return SSHPath(path, ssh=self.ssh)

    # TODO: check
    def cwd(self):
        """ Return a new path pointing to the "current working directory"
        for this SFTP session
        """
        return self.new(self.sftp.getcwd())

    # TODO: check
    def home(self):
        """ Return a new path pointing to the user's home directory on remote
        """
        return self.new(self.ssh.home)

    def rmdir(self, recursive: bool = False):
        """ Remove this directory.

        Optionally do it recursively.
        """
        if recursive:
            for p in self.iterdir():
                if p.is_dir():
                    p.rmdir(recursive=True)
                else:
                    p.unlink()
            # if directory is empty
            super().rmdir()
        else:
            super().rmdir()

    def open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None) -> paramiko.SFTPFile:
        """ Open a file on the remote server

        Args:
            mode (str, optional): [description]. Defaults to 'r'. The Python 'b' flag is ignored, since SSH treats all files as binary.
            buffering (int, optional): [description]. Defaults to -1.
            encoding ([type], optional): [description]. Defaults to None.
            errors ([type], optional): [description]. Defaults to None.
            newline ([type], optional): [description]. Defaults to None.

        Returns:
            paramiko.SFTPFile: [description]
        """
        if encoding:
            raise RuntimeError(
                f"{self.__class__.__name__} doesn't support an 'encoding' parameter. "
                f"The encoding of the file is assumed to be UTF-8."
            )
        if errors:
            raise RuntimeError(
                f"{self.__class__.__name__} doesn't support an 'errors' parameter."
            )
        if newline:
            raise RuntimeError(
                f"{self.__class__.__name__} doesn't support an 'newline' parameter."
            )
        fp = self.sftp.open(str(self), mode=mode, bufsize=buffering)
        if 'r' in mode:
            fp.prefetch()
        return fp

    def read_text(self, *args, **kwargs) -> str:
        """ SSH treats all files as binary

        Returns:
            str: read result
        """
        return super().read_text(*args, kwargs).decode(encoding='utf-8')

    def touch(self, exist_ok=True):
        try:
            with self.open(mode='x'):
                pass
        except OSError:
            if exist_ok:
                self.sftp.utime(str(self), None)
            else:
                raise FileExistsError(str(self))

    def rename(self, target):
        return self.new(super().rename(target))

    def replace(self, target):
        return self.new(super().replace(target))

    # def glob(self, pattern: str):
    #     return fnmatch.filter(self.sftp.listdir(str(self)), pattern)

    # def recursive_iterdir(self, l = None):
    #     if not l: l = []
    #     if self.is_dir():
    #         for p in self.iterdir():
    #             if p.is_dir():
    #                 l.extend(p.recursive_iterdir(l))
    #             else:
    #                 l.append(p)
    #     else:
    #         l.append(self)
    #     return l
    # def rglob(self, pattern: str):
    #     l = self.recursive_iterdir()
    #     return fnmatch.filter(map(str, l), pattern)

    def get(self, localpath):
        self.sftp.get(str(self), localpath)

    def put(self, localpath) -> paramiko.SFTPAttributes:
        return self.sftp.put(localpath, str(self))
