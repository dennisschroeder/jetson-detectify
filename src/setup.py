# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('main/application.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="jetson-detectify",
    packages=["main"],
    install_requires=['Click', 'undictify', 'ruamel.yaml'],
    entry_points={
        "console_scripts": ['jetson-detectify = main.application:cli', 'jd = main.application:cli']
    },
    version=version,
    description="Run controllable object detection on a Nvidia Jetson Nano",
    long_description=long_descr,
    author="Dennis Schröder",
    author_email="dennisschroeder@me.com",
    url="https://github.com/dennisschroeder/jetson-detectify",
)