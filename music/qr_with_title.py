#!/usr/bin/env python3

import qrcode
from PIL import Image, ImageDraw, ImageFont
import zbarlight
from find_font import find_font
from sys import argv

title, text, filename = argv[1:4]
# QRコードを生成
qr = qrcode.QRCode(version=7, box_size=3, border=0, error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(text)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# テキストを設定
font_size = 3 * 4
font = find_font(r"YuGothic-Bold.*", font_size)

# パディング量（ピクセル単位）
padding = 3 * 2

# 描画用のオブジェクトを作成
draw = ImageDraw.Draw(qr_img)

# テキストの境界ボックスを取得
title_bbox = draw.textbbox((0, 0), title, font=font)
title_width = title_bbox[2] - title_bbox[0]
title_height = title_bbox[3] - title_bbox[1]

# テキストの背景に白い矩形を描画
x = (qr_img.width - (title_width + 2 * padding)) // 2
y = (qr_img.height - (title_height + 2 * padding)) // 2
draw.rectangle(
    [x, y, x + title_width + 2 * padding, y + title_height + 2 * padding],
    fill="white"
)

# テキストを中央に描画
draw.text((x + padding, y + padding), title, fill="black", font=font)

# デコード可能性を検証
def is_qr_decodable(image):
    """QRコードがデコード可能かを確認する"""
    try:
        # 画像をグレースケールに変換
        grayscale = image.convert("L")
        # QRコードをデコード
        decoded = zbarlight.scan_codes("qrcode", grayscale)
        return decoded is not None
    except Exception as e:
        print(f"Error during decoding: {e}")
        return False

qr_img.show()
qr_img.save(f"{filename}.qrcode.png")

# デコードチェック
if not is_qr_decodable(qr_img):
    raise ValueError("The QR code with title overlay is not decodable!")

# 成功時に表示
