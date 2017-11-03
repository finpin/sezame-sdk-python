#!/usr/bin/python3

from sezame import manager
import sezame.stores as stores
import qrcode
import os

store = stores.File()
manager = manager.Manager(store)
manager.startup()

if not manager.is_ready():
    print("sezame not ready")
    exit(-1)

client = manager.get_client('https://hqfrontend-dev.seza.me/')

username = os.environ['USER']

r = client.link_status(username)
if not r.is_linked():
    r = client.link(username)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(r.get_qrcode_data())
    qr.make(fit=True)
    # qr.print_ascii()
    f = open('pairing-qr.png', 'w')
    img = qr.make_image()
    img.save(f.buffer, 'png')
else:
    print("alread paired")
