from dataclasses import dataclass
from typing import Optional

from .. import RoutePath, PayLoad, ObjectId, EntityCommand
from undictify import type_checked_constructor


@type_checked_constructor(convert=True)
@dataclass
class Route:
    path: RoutePath
    payload: PayLoad = b''


@type_checked_constructor(convert=True)
@dataclass
class RouterMessage:
    target: ObjectId
    command: Optional[EntityCommand]
    payload: PayLoad = b''
