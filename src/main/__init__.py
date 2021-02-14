from dataclasses import dataclass
from typing import NewType, List

from peewee import SqliteDatabase
from playhouse.signals import Model
from undictify import type_checked_constructor

from .configuration.models import ApplicationConfig

CliCommand = NewType('CliCommand', list)
DirPath = NewType('DirPath', str)
FilePath = NewType('FilePath', str)
Host = NewType('Host', str)
Port = NewType('Port', int)
ModuleName = NewType('ModuleName', str)
Topic = NewType('Topic', str)
DeviceId = NewType('DeviceId', str)
RoutePath = NewType('RoutePath', str)
PayLoad = NewType('PayLoad', bytes)
EntityDomain = NewType('EntityDomain', str)
ObjectId = NewType('ObjectId', str)
EntityCommand = NewType('EntityCommand', str)
RoutePathElements = NewType('RoutePathElements', List[str])
CommandIndex = NewType('CommandIndex', int)

db = SqliteDatabase("jd.db")


class BaseModel(Model):
    class Meta:
        database = db


@type_checked_constructor(convert=True)
@dataclass
class ApplicationContext:
    config: ApplicationConfig
    device_id: DeviceId
