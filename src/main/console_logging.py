import enum
import sys
from datetime import datetime
from enum import Enum

import click


def print_blank_line():
    click.echo("")


def print_error_message(error_message: str):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    click.secho(f"{now} - ERROR: {error_message}", err=True, fg=_Color.RED.value)


def print_info_message(title: str):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    click.secho(f"{now} - INFO: {title}")


def print_info_header(title: str):
    click.secho(f":: {title} ::", bg=_Color.WHITE.value, fg=_Color.BLACK.value)


def print_info_footer(title: str):
    click.secho(f":: {title} ::", bg=_Color.WHITE.value, fg=_Color.BLACK.value)
    print_blank_line()


def print_upcoming_step(message: str):
    # Using python standard print function cause click.echo does not provided end parameter
    print(f"|  ☛  {message}", end="\r")


def print_success_step(title: str):
    click.secho(f"|  ✔  {title}", fg=_Color.GREEN.value)


def print_error_step(title: str):
    click.secho(f"|  ✘  {title}", err=True, fg=_Color.RED.value)


def print_step_separator():
    click.echo("|")


def print_just_text(content: str):
    click.echo(content)



@enum.unique
class _Color(Enum):
    RED = "red"
    BLACK = "black"
    WHITE = "white"
    GREEN = "green"
