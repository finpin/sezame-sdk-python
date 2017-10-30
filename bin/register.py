#!/usr/bin/python3

from sezame import manager
import sezame.stores as stores

store = stores.File()
manager = manager.Manager(store)
manager.startup()

if manager.is_ready():
    print("sezame is ready")
    exit(0)

client = manager.get_client('https://hqfrontend-dev.seza.me/')
regData = client.register('reg@bretterklieber.com', 'pytest')
manager.config = regData.data
manager.save()
