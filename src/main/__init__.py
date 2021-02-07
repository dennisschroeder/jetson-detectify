import os
from typing import NewType

CliCommand = NewType('CliCommand', list)
DirPath = NewType('DirPath', str)
FilePath = NewType('FilePath', str)
Host = NewType('Host', str)
Port = NewType('Port', int)
ModuleName = NewType('ModuleName', str)