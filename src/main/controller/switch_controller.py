import time
from typing import List, Optional

from ..router.models import RouterMessage

from .. import EntityCommand, PayLoad


def switch_controller(route_message: RouterMessage) -> Optional[List[RouterMessage]]:

    if route_message.command == "set":
        if route_message.payload == b'ON':
            return [RouterMessage(target=route_message.target, command=EntityCommand("state"), payload=PayLoad(b'ON'))]

        if route_message.payload == b'OFF':
            return [RouterMessage(target=route_message.target, command=EntityCommand("state"), payload=PayLoad(b'OFF'))]

