#!/usr/bin/python3

import inspect
import os
import sys
import syslog
import time

moduledir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "..")))
if moduledir not in sys.path:
    sys.path.insert(0, moduledir)

from sezame import manager
import sezame.stores as stores

# set to None vor live system
endpoint = 'https://hqfrontend-dev.seza.me/'

syslog.openlog(ident="pam_sezame", logoption=syslog.LOG_PID, facility=syslog.LOG_AUTH)

store = stores.File('/etc/sezame/')
manager = manager.Manager(store)
manager.startup()

if not manager.is_ready():
    syslog.syslog(syslog.LOG_ERR, "sezame not ready")
    exit(-1)

try:
    username = os.environ['PAM_USER']
    syslog.syslog(syslog.LOG_INFO, "authenticate: " + os.environ['PAM_USER'])
    client = manager.get_client(endpoint)

    r = client.auth(username)
    if r.is_notfound():
        syslog.syslog(syslog.LOG_INFO, "user: " + os.environ['PAM_USER'] + ' not paired')
        exit(-1)

    r = client.auth(username)
    if r.is_ok():
        for i in range(0, 20):
            status = client.auth_status(r.get_id())
            print(status.get_status())
            if status.is_authorized():
                exit(0)

            if status.is_denied():
                syslog.syslog(syslog.LOG_INFO, "user denied the request")
                exit(-1)

            time.sleep(1)

        syslog.syslog(syslog.LOG_INFO, "user not responded in time")
        exit(-1)

except KeyError as e:
    syslog.syslog(syslog.LOG_ERR, "error reading PAM_USER environment " + str(e))

exit(-1)
