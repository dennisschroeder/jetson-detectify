# -*- coding: utf-8 -*-

""" main.application: provides all cli commands."""

import sys

from .mqtt.client import start_connection, start_mqtt_connection_blocking
from undictify import type_checked_call
from typing import Optional, NewType, List
from io import BufferedReader
import click
from .application_checks import check_jetson_python_module_availability, check_general_host_availability, \
    check_if_application_init_process_ran_successfully
from .console_logging import print_info_header, print_blank_line, print_step_separator, print_info_footer
from .initialization import ApplicationSettings, create_with_settings, write_init_report_to
from .configuration.config import load_application_config, ApplicationConfig

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
def init():
    print_info_header("Starting the initialization process")
    print_step_separator()

    default_settings: ApplicationSettings = ApplicationSettings.create_default()
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

    app_config: ApplicationConfig = load_application_config(config)

    startup_checks: List[bool] = [
        check_if_application_init_process_ran_successfully(),
        check_jetson_python_module_availability(),
        check_general_host_availability(app_config)
    ]

    print_step_separator()

    if False in startup_checks:
        print_info_footer("Startup process failed!")
        sys.exit(1)

    print_info_header("Startup process successful!")
    print_blank_line()

    print_info_header("Connecting to the MQTT Broker")
    print_step_separator()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    start_mqtt_connection_blocking(app_config)





