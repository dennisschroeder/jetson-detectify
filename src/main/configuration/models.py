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
class ApplicationConfig:
    mqtt_broker: MqttBroker


@type_checked_constructor(skip=True)
@dataclass
class InitData:
    success: bool
    last_init_run: str
