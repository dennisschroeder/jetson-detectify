# -*- coding: utf-8 -*-

""" .config.models: provides config model objects."""

from dataclasses import dataclass
from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class MqttBroker:
    username: str
    password: str
    host: str
    port: int


@type_checked_constructor()
@dataclass
class CoreConfig:
    mqtt_broker: MqttBroker
