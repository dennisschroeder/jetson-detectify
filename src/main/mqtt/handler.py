import json
import sys
from typing import NewType, Any, Dict, List
from paho.mqtt.client import MQTTMessage, Client
from undictify import type_checked_call

from main.router.routing import Route, route_to_controller
from .. import ApplicationContext, RoutePath, PayLoad, Topic, DeviceId
from ..console_logging import print_info_message, print_error_message, print_success_message

_MqttErrorCode = NewType("MqttErrorCode", int)


def on_connect(client, app_ctx: ApplicationContext, flags, rc):
    if rc != 0:
        print_error_message(_resolve_mqtt_connection_result(rc))
        sys.exit(1)

    print_success_message(_resolve_mqtt_connection_result(rc))
    root_topic = Topic(app_ctx.config.mqtt_broker.root_topic)
    device_id = DeviceId(app_ctx.device_id)

    payload = {"name": "Jetson Detectify", "command_topic": f"{root_topic}/switch/{device_id}/jetson_detectify/set",
               "state_topic": f"{root_topic}/switch/{device_id}/jetson_detectify/state"}
    client.publish(topic=f"{root_topic}/switch/{device_id}/jetson_detectify/config", payload=json.dumps(payload))
    client.subscribe(f"{root_topic}/switch/+/jetson_detectify/#", 1)


@type_checked_call()
def on_message(client: Client, app_ctx: ApplicationContext, mqtt_message: MQTTMessage):
    print_info_message(f"Topic: {mqtt_message.topic} -> {mqtt_message.payload}")

    route = Route(path=RoutePath(mqtt_message.topic), payload=PayLoad(mqtt_message.payload))
    return_routes: List[Route] = route_to_controller(route=route, app_ctx=app_ctx)

    for route in return_routes:
        client.publish(topic=route.path, payload=route.payload)


@type_checked_call(convert=True)
def _resolve_mqtt_connection_result(code: _MqttErrorCode) -> str:
    return {
        0: "Connection successfully established",
        1: "Connection refused – incorrect protocol version",
        2: "Connection refused – invalid client identifier",
        3: "Connection refused – server unavailable",
        4: "Connection refused – bad username or password",
        5: "Connection refused – not authorised"
    }.get(code, f"Unknown error with code {code}")


def _deserialize_payload(mqtt_message: MQTTMessage) -> Dict[str, Any]:
    return json.loads(mqtt_message.payload.decode("utf-8"))
