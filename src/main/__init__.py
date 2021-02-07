import os
from typing import NewType

CliCommand = NewType('CliCommand', list)
DirPath = NewType('DirPath', str)
FilePath = NewType('FilePath', str)
DEFAULT_CONFIG_FILE_PATH = FilePath(os.path.expanduser("~/.jetson_detectify/application.yaml"))