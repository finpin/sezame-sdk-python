#!/usr/bin/python3

from sezame import manager
import sezame.stores as stores
import qrcode

store = stores.File()
manager = manager.Manager(store)
manager.startup()

if not manager.is_ready():
    print("sezame not ready")
    exit(-1)

client = manager.get_client('https://hqfrontend-dev.seza.me/')

r = client.link_delete("sepp")
if r.is_ok():
    print("pairing removed")
    exit(0)

if r.is_notfound():
    print("user not paired")
    exit(-1)
