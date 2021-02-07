# -*- coding: utf-8 -*-

""" main.application: provides all cli commands."""
import sys

import click
from main import Host, Port
from main.util import is_host_port_open, test

from .console_logging import print_info_header, print_blank_line, print_step_separator, print_error_step, \
    print_info_footer, print_upcoming_step, print_success_step
from .initialization import create_default_settings, ApplicationSettings, create_with_settings, write_init_report_to

from undictify import type_checked_call
from typing import Optional, NewType
from io import BufferedReader
from .configuration.config import load_application_config

__version__ = "0.1.0"
SomeType = NewType("SomeType", str)


@click.group()
def cli():
    click.secho(f":: JetsonDetectify Version: {__version__} ::", fg="black", bg="green")
    print_blank_line()


@cli.command()
def debug():
    pass


@cli.command()
@type_checked_call()
def init():
    print_info_header("Starting the initialization process")
    print_step_separator()

    default_settings: ApplicationSettings = create_default_settings()
    create_with_settings(default_settings)
    print_step_separator()
    write_init_report_to(default_settings.application_storage_dir)

    print_step_separator()
    print_info_header("Initialization process successful")


@cli.command()
@click.option(
    "--config",
    "-c", type=click.File("rb"),
    required=False,
    help="Provides an alternative path to the config file."
)
@type_checked_call()
def start(config: Optional[BufferedReader]):
    """ Starts the application"""
    print_info_header("Starting Jetson-Detectify")
    print_step_separator()

    config = load_application_config(config)

    print_upcoming_step("Checking host availability")
    if not is_host_port_open(Host(config.mqtt_broker.host), Port(config.mqtt_broker.port)):
        print_error_step(f"Host availability check to {config.mqtt_broker.host}:{config.mqtt_broker.port} "
                         "failed! Please Check your settings in application.yaml")
        print_step_separator()
        print_info_footer("Starting Jetson-Detectify failed")
        sys.exit(1)

    print_success_step(f"Host availability check to {config.mqtt_broker.host}:{config.mqtt_broker.port} succeeded!")
    print_step_separator()



