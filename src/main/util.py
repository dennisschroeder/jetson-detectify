import os
import subprocess
from .console_logging import print_error_message

from . import CliCommand, DirPath, FilePath


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


def write_file_to(file_path: FilePath, content: str):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except IOError as error:
        raise FileCreationException(error)


class DirectoryCreationException(Exception):
    def __init__(self, cause: OSError):
        self.cause = cause


class FileCreationException(IOError):
    def __init__(self, cause: OSError):
        self.cause = cause
