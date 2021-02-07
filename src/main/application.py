# -*- coding: utf-8 -*-

""" main.application: provides all cli commands."""
import click

from .console_logging import print_info_header, print_blank_line, print_step_separator
from .initialization import create_default_settings, ApplicationSettings, create_with_settings

from undictify import type_checked_call
from typing import Optional
from io import BufferedReader
from .configuration.config import load_application_config


__version__ = "0.1.0"


@click.group()
def cli():
    click.secho(f":: JetsonDetectify Version: {__version__} ::", fg="black", bg="green")
    print_blank_line()


@cli.command()
@click.option("--default", "-d", is_flag=True, help="When set, this init process uses the default config")
def init(default: bool):
    print_info_header("Starting the initialization process")
    print_step_separator()
    if default:
        default_settings: ApplicationSettings = create_default_settings()
        create_with_settings(default_settings)
    print_step_separator()
    print_info_header("Initialization process successful")


@cli.command()
@click.option(
    "--config",
    "-c", type=click.File("rb"),
    required=False,
    help="Provide an alternative path to the config file."
)
@type_checked_call()
def start(config: Optional[BufferedReader]):
    """ Starts the application"""
    config = load_application_config(config)
    click.echo(config)
