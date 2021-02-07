import json
import os
import subprocess
import sys
from typing import Dict, Any, TypeVar, Type

from main.configuration.models import InitData
from undictify import type_checked_call, type_checked_constructor
from .console_logging import print_error_message
from . import CliCommand, DirPath, FilePath, Host, Port, ModuleName


@type_checked_call()
def run_cli_command(command: CliCommand) -> bytes:
    try:
        return subprocess.check_output(command)
    except subprocess.CalledProcessError:
        print_error_message(f"Calling subprocess {command} resulted in an error!")
        sys.exit(1)


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


def read_application_init_data(file_path: FilePath) -> InitData:
    with open(file_path, 'r') as file:
        json_string = json.load(file)

    return InitData(**json_string)


@type_checked_constructor()
class DirectoryCreationException(Exception):
    def __init__(self, cause: OSError):
        self.cause = cause


@type_checked_constructor()
class FileCreationException(Exception):
    def __init__(self, cause: OSError):
        self.cause = cause
