#!/usr/bin/env python3

import qrcode

qr = qrcode.QRCode(box_size=3)
qr.add_data("日本語")
qr.make()
img = qr.make_image()
img.show()
