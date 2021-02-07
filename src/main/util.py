import json
import os
import socket
import subprocess
from contextlib import closing
from typing import Dict, Any

from undictify import type_checked_call, type_checked_constructor

from .console_logging import print_error_message

from . import CliCommand, DirPath, FilePath, Host, Port


@type_checked_call()
def run_cli_command(command: CliCommand) -> bytes:
    try:
        return subprocess.check_output(command)
    except subprocess.CalledProcessError:
        print_error_message(f"Calling subprocess {command} resulted in an error!")


def create_directory(dir_path: DirPath):
    try:
        os.mkdir(dir_path)
    except OSError as error:
        raise DirectoryCreationException(error)


def create_file_from_str_to(file_path: FilePath, content: str):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except IOError as error:
        raise FileCreationException(error)


def create_file_from_dict_to(file_path: FilePath, content: Dict[str, Any]):
    try:
        with open(file_path, "w") as file:
            file.write(json.dumps(content, indent=4))
    except IOError as error:
        raise FileCreationException(error)


@type_checked_constructor()
class DirectoryCreationException(Exception):
    def __init__(self, cause: OSError):
        self.cause = cause


@type_checked_constructor()
class FileCreationException(Exception):
    def __init__(self, cause: OSError):
        self.cause = cause


def is_host_port_open(host: Host, port: Port) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        if sock.connect_ex((host, port)) == 0:
            return True
    return False


def test():
    import jetson.inference
    print("TEST")