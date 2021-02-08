import json
from dataclasses import dataclass
from typing import NewType, Any, Optional

from paho.mqtt.client import MQTTMessage, Client
from undictify import type_checked_call, type_checked_constructor

from ..console_logging import print_info_message, print_error_message, print_success_message

_MqttErrorCode = NewType("MqttErrorCode", int)


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print_error_message(_resolve_mqtt_connection_result(rc))
    else:
        print_success_message(_resolve_mqtt_connection_result(rc))
        client.subscribe("#", 0)


@type_checked_call()
def on_message(client: Client, userdata: Optional[Any], msg: MQTTMessage):
    payload_dict = json.loads(msg.payload)
    print_info_message(f"Topic: {msg.topic} -> {payload_dict}")


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

