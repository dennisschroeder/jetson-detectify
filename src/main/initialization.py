import os
from dataclasses import dataclass

from . import FilePath, DirPath
from .util import create_directory, FileCreationException, DirectoryCreationException, write_file_to
from .console_logging import print_info_step, print_error_step


@dataclass
class ApplicationSettings:
    application_base_dir: DirPath
    application_storage_dir: DirPath
    application_settings_file: FilePath


def create_default_settings() -> ApplicationSettings:
    return ApplicationSettings(
        application_base_dir=DirPath(os.path.expanduser("~/.jetson_detectify")),
        application_storage_dir=DirPath(os.path.expanduser("~/.jetson_detectify/.storage")),
        application_settings_file=FilePath(os.path.expanduser("~/.jetson_detectify/application.yaml"))
    )


def create_with_settings(settings: ApplicationSettings):

    create_application_directory(settings.application_base_dir)
    create_application_directory(settings.application_storage_dir)

    content = """mqttBroker:
    username: username
    password: password
    host: localhost
    port: 1883
    """
    create_application_file(settings.application_settings_file, content)


def create_application_directory(dir_path: DirPath):
    if not os.path.exists(dir_path):
        try:
            create_directory(dir_path)
            print_info_step(f"Creating directory [{dir_path}] succeeded")
            return
        except DirectoryCreationException as error:
            print_error_step(f"Creating directory [{dir_path}] failed! OS error({error.cause.strerror}): {error.cause.strerror}")

    print_info_step(f"Directory [{dir_path}] already exists!")


def create_application_file(file_path: FilePath, content: str):
    if not os.path.exists(file_path):
        try:
            write_file_to(file_path=file_path, content=content)
            print_info_step(f"Creating file [{file_path}] succeeded")
        except FileCreationException as error:
            print_error_step(f"Creating file [{file_path}] failed! I/O error({error.cause.errno}): {error.cause.strerror}")

    print_info_step(f"File [{file_path}] already exists!")
