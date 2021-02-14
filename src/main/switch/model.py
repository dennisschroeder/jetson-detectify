from peewee import CharField

from .. import BaseModel


class Switch(BaseModel):
    name: str = CharField(unique=True)
