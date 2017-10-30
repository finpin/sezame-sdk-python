#!/usr/bin/python3

from sezame import manager
import sezame.stores as stores
import time

store = stores.File()
manager = manager.Manager(store)
manager.startup()

if not manager.is_ready():
    print("not ready")
    exit(-1)

client = manager.get_client('https://hqfrontend-dev.seza.me/')

r = client.auth('susi')
if r.is_notfound():
    print("user not paired")

# r = client.auth('sepp', authtype='fraud')
r = client.auth('sepp')
if r.is_ok():
    for i in range(0, 20):
        status = client.auth_status(r.get_id())
        print(status.get_status())
        if status.is_authorized():
            print("authorized")
            exit(0)

        if status.is_denied():
            print("denied")
            exit(0)

        time.sleep(1)

    print("timeout")
    exit(-1)
