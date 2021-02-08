import sys

import paho.mqtt.client as mqtt
from undictify import type_checked_call

from .handler import on_connect, on_message
from ..console_logging import print_info_footer
from ..configuration.models import ApplicationConfig

_JETSON_DETECTIFY_CLIENT_NAME = "jetson_detectify"


@type_checked_call(convert=True)
def start_mqtt_connection_blocking(app_config: ApplicationConfig):
    connection = start_connection(app_config)
    try:
        connection.loop_forever()
    except KeyboardInterrupt:
        connection.disconnect()
        print_info_footer("Disconnected from MQTT Broker ")
        sys.exit(0)


@type_checked_call(convert=True)
def start_connection(app_config: ApplicationConfig) -> mqtt.Client:
    client = _create_mqtt_client(app_config)
    client.connect(host=app_config.mqtt_broker.host, port=app_config.mqtt_broker.port)
    client.on_connect = on_connect
    client.on_message = on_message
    return client


@type_checked_call(convert=True)
def _create_mqtt_client(app_config: ApplicationConfig) -> mqtt.Client:
    client = mqtt.Client(_JETSON_DETECTIFY_CLIENT_NAME)
    client.username_pw_set(username=app_config.mqtt_broker.username, password=app_config.mqtt_broker.password)
    return client
