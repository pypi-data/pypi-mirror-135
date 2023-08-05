import paramiko
import getpass
from typing import Optional
from pathliberty import ssh_config

def get_ssh_client(
    dest_host: str,
    *,
    username: str = getpass.getuser(),
    password: Optional[str] = None,
    dest_port: Optional[int] = None,
) -> paramiko.SSHClient:
    """ Get a high-level representation of a open session with an SSH server.

    This object can be used as contextmanager::

        with get_ssh_client('hostname') as client:
            stdin, stdout, stderr = client.exec_command('ls -al')
            print(stdout.read().decode("utf-8"))

    Args:
        dest_host (str): target host
        username (str): the username to authenticate as
        password (str): Used for password authentication
        dest_port (int, optional): target port. If None, it will be a ssh_config.DEFAULT_PORT.

    Returns:
        paramiko.SSHClient: Object of  :class:`~paramiko.SSHClient`
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=dest_host,
        username=username,
        password=password,
        port=dest_port or ssh_config.DEFAULT_PORT,
        timeout=ssh_config.DEFAULT_PORT
    )
    return client

def get_ssh_client_through_proxy(
    dest_host: str,
    *,
    jump_host: str,
    username: str = getpass.getuser(),
    password: Optional[str] = None,
    dest_port: Optional[int] = None,
    jump_port: Optional[int] = None,
) -> paramiko.SSHClient:
    """ Get a high-level representation of a open session with an SSH server via jump-host

    This object can be used as contextmanager.

    Args:
        dest_host (str): target host
        jump_host (str): jump host used as transport
        username (str): the username to authenticate as
        password (str): Used for password authentication
        dest_port (int, optional): target port. If None, it will be a ssh_config.DEFAULT_PORT.
        jump_port (int, optional): jump port. If None, it will be a ssh_config.DEFAULT_PORT.

    Returns:
        paramiko.SSHClient: Object of :class:`~paramiko.SSHClient`
    """
    dest_port = dest_port or ssh_config.DEFAULT_PORT
    jump_port = jump_port or ssh_config.DEFAULT_PORT
    
    jclient = paramiko.SSHClient()
    jclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jclient.connect(hostname=jump_host, username=username, password=password, port=jump_port, timeout=ssh_config.DEFAULT_CONNECTION_TIMEOUT)

    jtransport = jclient.get_transport()
    dest_addr = (dest_host, dest_port)
    local_addr = (jump_host, jump_port)
    jchannel = jtransport.open_channel("direct-tcpip", dest_addr, local_addr, timeout=ssh_config.DEFAULT_CONNECTION_TIMEOUT)

    target = paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    target.connect(
        hostname=jump_host,
        username=username,
        port=jump_port,
        sock=jchannel,
        password=password,
        timeout=ssh_config.DEFAULT_CONNECTION_TIMEOUT
    )

    return target

def get_ssh(
    dest_host: str,
    *,
    username: str = getpass.getuser(),
    password: Optional[str] = None,
    dest_port: Optional[int] = None,
    jump_host: Optional[str] = None,
    jump_port: Optional[int] = None,
) -> paramiko.SSHClient:

    try:
        if jump_host:
            client = get_ssh_client_through_proxy(
                dest_host=dest_host,
                dest_port=dest_port,
                username=username,
                password=password,
                jump_host=jump_host,
                jump_port=jump_port,
            )
        else:
            client = get_ssh_client(
                dest_host=dest_host,
                dest_port=dest_port,
                username=username,
                password=password,
            )
    except paramiko.AuthenticationException as e:
        base_msg = e.args[0]
        if not password:
            raise RuntimeError(f"{base_msg} Try to use password or check your keys")
        else:
            raise RuntimeError(f"{base_msg} Check your password or try to use keys")

    else:
        return client

class SSHSession:
    def __init__(
        self,
        dest_host: str,
        *,
        username: str = getpass.getuser(),
        password: Optional[str] = None,
        dest_port: Optional[int] = None,
        jump_host: Optional[str] = None,
        jump_port: Optional[int] = None,
    ):

        self.client = get_ssh(
            dest_host,
            username=username,
            password=password,
            dest_port=dest_port,
            jump_host=jump_host,
            jump_port=jump_port,
        )

        self.host = dest_host
        self.proxy = jump_host

        self._sftp_open = False

    @property
    def sftp(self) -> paramiko.SFTPClient:
        if not self._sftp_open:
            self._sftp = self.client.open_sftp()
            self._sftp_open = True

        return self._sftp

    def __del__(self):
        self.client.close()

    def exec(self, command: str) -> str:
        _, stdout, stderr = self.client.exec_command(
            command=command,
            timeout=ssh_config.DEFAULT_CONNECTION_TIMEOUT
        )

        status = stdout.channel.recv_exit_status()

        if not status:
            return stdout.read().decode().strip()
        else:
            raise RuntimeError(stderr.read().decode())

    @property
    def home(self):
        return self.exec('echo ~').strip()
