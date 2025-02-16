#!/usr/bin/env python3

import qrcode
from sys import argv

box_size = 3
version = 1

text, filename = argv[1:3]
# QRコードを生成
qr = qrcode.QRCode(version=version, box_size=box_size, border=0, error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(text)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

qr_img.show()
qr_img.save(f"{filename}.qrcode.png")
