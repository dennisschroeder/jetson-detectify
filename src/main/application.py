# -*- coding: utf-8 -*-

""" main.application: provides all cli commands."""
import sqlite3
import sys
from io import BufferedReader
from typing import Optional, List
import click
from main import ApplicationContext, DeviceId, db
from main.database import connect_to_database, create_tables
from main.switch.model import Switch
from playhouse.signals import post_save
from undictify import type_checked_call
from .application_checks import check_jetson_python_module_availability, check_general_host_availability, \
    check_if_application_init_process_ran_successfully
from .configuration.config import load_application_config, ApplicationConfig
from .console_logging import print_info_header, print_blank_line, print_step_separator, print_info_footer
from .initialization import ApplicationSettings, create_application_settings_file, write_init_report_to, \
    create_sensors_config_file, create_default_application_settings
from .mqtt.client import start_mqtt_connection_blocking

__version__ = "0.1.0"


@click.group()
def cli():
    click.secho(f":: JetsonDetectify Version: {__version__} ::", fg="black", bg="green")
    print_blank_line()


@cli.command()
def debug():
    # print("Tell me what to do!")

    @post_save(sender=Switch)
    def on_save_handler(sender, instance: Switch, created):
        print(instance.name)

    jd = Switch.get_by_id(1)
    jd.name = "jd"
    jd.save()


@cli.command()
def init():
    print_info_header("Starting the initialization process")
    print_step_separator()

    default_settings: ApplicationSettings = create_default_application_settings()
    create_application_settings_file(default_settings)
    create_sensors_config_file(default_settings)
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
    print_info_header("Starting the Application")
    print_step_separator()

    app_config: ApplicationConfig = load_application_config(config)
    app_ctx = ApplicationContext(config=app_config, device_id=DeviceId("12345"))

    # noinspection PyTypeChecker
    startup_sequence_results: List[bool] = [
        check_if_application_init_process_ran_successfully(),
        check_jetson_python_module_availability(),
        check_general_host_availability(app_config),
        connect_to_database(),
        create_tables([Switch])
    ]

    print_step_separator()

    if False in startup_sequence_results:
        print_info_footer("Startup process failed!")
        sys.exit(1)

    print_info_header("Startup process successful!")
    print_blank_line()

    print_info_header("Connecting to the MQTT Broker")
    print_step_separator()

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    start_mqtt_connection_blocking(app_ctx)
