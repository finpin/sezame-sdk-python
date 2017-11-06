#!/usr/bin/python3

import tkinter as tk
import tkinter.font as font

from sezame import manager
import sezame.stores as stores
import qrcode
import getpass
import webbrowser

from io import BytesIO
from os import path

BASEDIR = path.dirname(__file__)

store = stores.File('/data/www/sezame/sezame-sdk/python/bin/')
sezame = manager.Manager(store)
sezame.startup()

sezame_environment = 'dev'

if not sezame.is_ready():
    print("not ready")
    exit(-1)

root = tk.Tk()
root.geometry('{}x{}'.format(800, 600))
root.wm_title("Sezame pairing")

defaultFont = font.Font(family="Helvetica", size=16, weight='bold')
root.option_add("*Font", defaultFont)


class Application(tk.Frame):
    def __init__(self, manager, master=None):
        super().__init__(master)
        self.manager = manager
        self.username = tk.StringVar()
        self.username.set(getpass.getuser())
        self.pair2_window = None
        self.pair2_canvas = None
        self.info_window = None
        self.info_canvas = None
        self.info_email = tk.StringVar()
        self.android_image = tk.PhotoImage(file=BASEDIR + '/images/android.png')
        self.ios_image = tk.PhotoImage(file=BASEDIR + '/images/ios.png')
        self.pair1()
        self.pack()

    def pair1(self):
        bg = tk.PhotoImage(file=BASEDIR + '/images/pair1.png')
        canvas_bg = tk.Label(self, image=bg)
        canvas_bg.background = bg
        canvas_bg.pack()

        input_username = tk.Entry(self, width=40, textvariable=self.username)
        input_username.place(x=115, y=310)

        btn_quit = tk.Label(self, text="EXIT", fg='white', bg='#ccc')
        btn_quit.place(x=35, y=505, width=120, height=54)
        btn_quit.bind("<Button-1>", lambda e,: root.destroy())

        btn_info = tk.Label(self, text="I DO NOT HAVE THE SEZAME APP YET", fg='white', bg='#29abe2')
        btn_info.place(x=200, y=504, width=395, height=55)
        btn_info.bind("<Button-1>", lambda e,: self.download_info())

        btn_next = tk.Label(self, text="NEXT", fg='white', bg='#ccc')
        btn_next.place(x=640, y=505, width=120, height=54)
        btn_next.bind("<Button-1>", lambda e,: self.pair2())

    def pair2(self):
        self.pair2_window = tk.Toplevel(self)
        self.pair2_window.title('Sezame QR Code')
        self.pair2_window.geometry('800x825')

        bg = tk.PhotoImage(file=BASEDIR + '/images/pair2.png')
        self.pair2_canvas = tk.Label(self.pair2_window, image=bg)
        self.pair2_canvas.background = bg
        self.pair2_canvas.pack()

        btn_back = tk.Label(self.pair2_window, text="BACK", fg='white', bg='#ccc')
        btn_back.place(x=35, y=755, width=120, height=54)
        btn_back.bind("<Button-1>", lambda e,: self.close_pair2())

        btn_quit = tk.Label(self.pair2_window, text="FINISH", fg='white', bg='#ccc')
        btn_quit.place(x=640, y=755, width=125, height=54)
        btn_quit.bind("<Button-1>", lambda e,: root.destroy())

        if not len(self.username.get()):
            return

        client = self.manager.get_client(environment=sezame_environment)

        r = client.link_status(self.username.get())
        if not r.is_linked():
            r = client.link(self.username.get())

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=7,
                border=4
            )
            qr.add_data(r.get_qrcode_data())
            qr.make(fit=True)
            img = qr.make_image()

            output = BytesIO()
            img.save(output, 'PNG')
            bg = tk.PhotoImage(data=output.getvalue())
            qr_canvas = tk.Label(self.pair2_window, image=bg, bg='white')
            qr_canvas.background = bg  # keep reference
            qr_canvas.place(x=10, y=330, width=400, height=400)

    def close_pair2(self):
        self.pair2_canvas.background = None  # dereference, let gc destroy the canvas
        self.pair2_window.destroy()

    def download_info(self):
        if self.info_window is not None:
            self.info_window.destroy()

        self.info_window = tk.Toplevel(self)
        self.info_window.title('Sezame mobile app')
        self.info_window.geometry('800x578')
        self.info_window.focus_set()

        bg = tk.PhotoImage(file=BASEDIR + '/images/appinfo.png')
        self.info_canvas = tk.Label(self.info_window, image=bg)
        self.info_canvas.background = bg
        self.info_canvas.pack()

        android_canvas = tk.Label(self.info_window, image=self.android_image, bg='#b3b3b3')
        android_canvas.place(x=105, y=312)
        android_canvas.bind("<Button-1>", lambda e,: webbrowser.open_new("https://seza.me/app/android"))

        ios_canvas = tk.Label(self.info_window, image=self.ios_image, bg='#b3b3b3')
        ios_canvas.place(x=410, y=312)
        ios_canvas.bind("<Button-1>", lambda e,: webbrowser.open_new("https://seza.me/app/ios"))

        btn_sendk = tk.Label(self.info_window, text="SEND", fg='white', bg='#628070')
        btn_sendk.place(x=587, y=485, width=180, height=54)
        btn_sendk.bind("<Button-1>", lambda e,: self.send_infoemail())

        input_email = tk.Entry(self.info_window, width=34, textvariable=self.info_email)
        input_email.place(x=120, y=493)

    def send_infoemail(self):
        return


app = Application(master=root, manager=sezame)
app.mainloop()
