#!/usr/bin/python3

from sezame import manager
import sezame.stores as stores
from sezame.certutil import CertUtil

store = stores.File()
manager = manager.Manager(store)
manager.startup()

if manager.is_ready():
    print("sezame is ready")
    exit(0)

private_key, csr = CertUtil.make_csr(manager.get_clientcode())

client = manager.get_client('https://hqfrontend-dev.seza.me/')
resp = client.sign(manager.get_sharedsecret(), csr)
if resp.is_notfound():
    print("please register first")
    exit(0)

manager.private_key = private_key
manager.certificate = resp.get_certificate()
manager.save()
