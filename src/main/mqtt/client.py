import sys
import paho.mqtt.client as mqtt
from ..database import disconnect_from_database

from .. import ApplicationContext
from undictify import type_checked_call

from .handler import on_connect, on_message
from ..console_logging import print_info_footer

_JETSON_DETECTIFY_CLIENT_NAME = "jetson_detectify"


@type_checked_call(convert=True)
def start_mqtt_connection_blocking(app_ctx: ApplicationContext):
    connection = _start_connection(app_ctx)
    try:
        connection.loop_forever()
    except KeyboardInterrupt:
        connection.disconnect()
        # ToDo: Needs to be moved to the application layer.
        disconnect_from_database()
        print_info_footer("Disconnected from MQTT Broker ")
        sys.exit(0)


@type_checked_call(convert=True)
def _start_connection(app_ctx: ApplicationContext) -> mqtt.Client:
    client = _create_mqtt_client(app_ctx)
    client.connect(host=app_ctx.config.mqtt_broker.host, port=app_ctx.config.mqtt_broker.port)
    client.on_connect = on_connect
    client.on_message = on_message
    return client


@type_checked_call(convert=True)
def _create_mqtt_client(app_ctx: ApplicationContext) -> mqtt.Client:
    client = mqtt.Client(client_id=_JETSON_DETECTIFY_CLIENT_NAME, userdata=app_ctx)
    client.username_pw_set(username=app_ctx.config.mqtt_broker.username, password=app_ctx.config.mqtt_broker.password)
    return client

