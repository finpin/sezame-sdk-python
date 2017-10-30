#!/usr/bin/python3

from sezame import manager

manager = manager.Manager()
manager.startup()

if not manager.is_ready():
    print("not ready")
    exit(-1)

client = manager.get_client('https://hqfrontend-dev.seza.me/')
client.cancel()

manager.cleanup()
