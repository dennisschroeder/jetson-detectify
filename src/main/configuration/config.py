# -*- coding: utf-8 -*-

""" main.configuration.config: privide"""
import os
import sys
from typing import Optional

from .. import FilePath
from ..initialization import create_default_application_settings
from undictify import type_checked_call
from ..util import print_error_message
from ruamel.yaml import YAML
from io import BufferedReader
from .models import ApplicationConfig

_DEFAULT_CONFIG_FILE_PATH: FilePath = create_default_application_settings().application_settings_file


@type_checked_call()
def load_application_config(custom_config: Optional[BufferedReader]) -> ApplicationConfig:
    yaml_parser = YAML()

    if custom_config:
        parsed_yaml = yaml_parser.load(custom_config)
        return ApplicationConfig(**parsed_yaml)

    if not does_default_config_exists(_DEFAULT_CONFIG_FILE_PATH):
        print_error_message(f"Could not find {_DEFAULT_CONFIG_FILE_PATH}")
        print_error_message(
            "Please run \"jetson-dictify init\" command and follow the instructions"
            "or set an alternative path with the \"--config path/to/custom/application.yaml\" command!"
        )
        sys.exit(1)

    with open(_DEFAULT_CONFIG_FILE_PATH, "r") as file:
        parsed_yaml = yaml_parser.load(file)

    return ApplicationConfig(**parsed_yaml)


def does_default_config_exists(path: FilePath) -> bool:
    return os.path.isfile(path)
