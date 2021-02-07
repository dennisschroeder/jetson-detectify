# -*- coding: utf-8 -*-

""" main.configuration.config: privide"""
import os
import sys
from typing import Optional
from undictify import type_checked_call
from ..util import print_error_message
from .. import FilePath, DEFAULT_CONFIG_FILE_PATH
from ruamel.yaml import YAML
from io import BufferedReader
from .models import CoreConfig


@type_checked_call()
def load_application_config(custom_config: Optional[BufferedReader]) -> CoreConfig:
    yaml_parser = YAML()

    if custom_config:
        parsed_yaml = yaml_parser.load(custom_config)
        return CoreConfig(**parsed_yaml)

    if not does_default_config_exists(DEFAULT_CONFIG_FILE_PATH):
        print_error_message(f"Could not find {DEFAULT_CONFIG_FILE_PATH}")
        print_error_message(
            "Please run \"jetson-dictify init\" command and follow the instructions"
            "or set an alternative path with the \"--config path/to/custom/application.yaml\" command!"
        )
        sys.exit(1)

    with open(DEFAULT_CONFIG_FILE_PATH, "r") as file:
        parsed_yaml = yaml_parser.load(file)

    return CoreConfig(**parsed_yaml)


def does_default_config_exists(path: FilePath) -> bool:
    return os.path.isfile(path)
