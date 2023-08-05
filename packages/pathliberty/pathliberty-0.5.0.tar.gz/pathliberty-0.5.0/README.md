# pathliberty
Extended object-oriented filesystem paths library.  
``pathliberty`` is the Python package that allows you to subclass a pathlib.PosixPath in a proper way.
To define your own custom path subclass, declare subclasses AbstractPathAccessor and AbstractPath.
## Features
Support SSH remote path via [Paramiko](https://pypi.org/project/paramiko/):
```python
from pathliberty import SSHPath
from pathliberty.ssh import SSHSession
from getpass import getuser

host = 'localhost'
ssh_session = SSHSession(
    host,
    password=******,
)
ssh_path = SSHPath(f'/home/{getuser()}', ssh=ssh_session)
assert ssh_path.parent == SSHPath('/home', host=host)
```

## Installation

```bash
pip install pathliberty
```