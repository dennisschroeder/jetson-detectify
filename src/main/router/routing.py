from enum import Enum
from functools import partial
from typing import List

from ..console_logging import print_error_message
from ..controller.switch_controller import switch_controller
from ..router.models import Route, RouterMessage
from undictify import type_checked_call

from .. import RoutePath, ApplicationContext, Topic, DeviceId, EntityDomain, ObjectId, RoutePathElements, CommandIndex


def _create_target_route_path(
        entity_domain: EntityDomain,
        root_topic: Topic,
        device_id: DeviceId
) -> RoutePath:
    return RoutePath(f"{root_topic}/{entity_domain}/{device_id}")


class BaseRoutePath(Enum):
    SWITCH = partial(_create_target_route_path, EntityDomain("switch"))
    SENSOR = partial(_create_target_route_path, EntityDomain("sensor"))
    CAMERA = partial(_create_target_route_path, EntityDomain("camera"))


@type_checked_call()
def route_to_controller(route: Route, app_ctx: ApplicationContext) -> List[Route]:
    root_topic = Topic(app_ctx.config.mqtt_broker.root_topic)
    device_id = DeviceId(app_ctx.device_id)

    switch_base_path = BaseRoutePath.SWITCH.value(root_topic, device_id)
    sensor_base_path = BaseRoutePath.SENSOR.value(root_topic, device_id)
    camera_base_path = BaseRoutePath.CAMERA.value(root_topic, device_id)

    if route.path.startswith(switch_base_path):
        to_controller_message = _create_router_message_from(route)
        from_controller_messages: List[RouterMessage] = switch_controller(to_controller_message)
        if from_controller_messages:
            return [_create_route_from(switch_base_path, message) for message in from_controller_messages]

    if route.path.startswith(sensor_base_path):
        print("Routed to SENSOR Controller")

    if route.path.startswith(camera_base_path):
        print("Routed to CAMERA Controller")

    return []


def _create_router_message_from(route: Route):
    path_elements: RoutePathElements = RoutePathElements(route.path.split("/"))

    command = None
    if _route_has_path_command(path_elements):
        command = path_elements[4]

    return RouterMessage(
        target=_extract_object_id_from_route_path(path_elements),
        payload=route.payload,
        command=command
    )


def _extract_object_id_from_route_path(route_path: RoutePathElements) -> ObjectId:
    object_id_index = 3
    try:
        return ObjectId(route_path[object_id_index])
    except IndexError:
        print_error_message(f"There is no ObjectId in path {route_path} at index {object_id_index}")


def _route_has_path_command(path_elements: List[str]) -> bool:
    return len(path_elements) == CommandIndex(5)


def _create_route_from(base_path: BaseRoutePath, router_message: RouterMessage) -> Route:
    final_path_string = f'{base_path}/{router_message.target}/{router_message.command}'
    return Route(path=RoutePath(final_path_string), payload=router_message.payload)
