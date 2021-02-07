import enum
from enum import Enum

import click


def print_blank_line():
    click.echo("")


def print_error_message(error_message: str):
    click.secho(f"ERROR: {error_message}", err=True, fg=Color.RED.value)


def print_info_message(title: str):
    click.secho(f"INFO: {title}")


def print_info_header(title: str):
    click.secho(f":: {title} ::", bg=Color.WHITE.value, fg=Color.BLACK.value)


def print_info_footer(title: str):
    click.secho(f":: {title} ::", bg=Color.WHITE.value, fg=Color.BLACK.value)
    print_blank_line()


def print_info_step(title: str):
    click.secho(f"|  ✔  {title}")


def print_error_step(title: str):
    click.secho(f"|  ✘  {title}")


def print_step_separator():
    click.echo("|")


@enum.unique
class Color(Enum):
    RED = "red"
    BLACK = "black"
    WHITE = "white"