from typing import List

from . import db
from .console_logging import print_upcoming_step, print_error_step, print_success_step
from peewee import ModelBase


def connect_to_database() -> bool:
    print_upcoming_step("Connecting to database!")
    connection_successful = db.connect()
    if not connection_successful:
        print_error_step("Connecting to database failed!")

    print_success_step("Connecting to database successful!")
    return connection_successful


def create_tables(tables: List[ModelBase]):
    print_upcoming_step("Creating database tables!")
    try:
        db.create_tables(tables)
        print_success_step("Table creation successful!")
    except Exception as error:
        print_error_step(f"Table creation failed! Cause: {str(error)}")


def disconnect_from_database() -> bool:
    print_upcoming_step("Disconnecting from database!")
    disconnecting_successful = db.close()
    if not disconnecting_successful:
        print_error_step("Disconnecting from database failed!")

    print_success_step("Disconnecting from database successful!")
    return disconnecting_successful
