#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import qrcode
from matplotlib import font_manager

def get_font_path_by_name(font_name):
    """フォント名とウェイトからフォントパスを取得する"""
    for font in font_manager.findSystemFonts(fontext='ttf'):
        # ファイル名に基づいて検索
        if font_name.lower() in font.lower():
            return font
    raise ValueError(f"指定したフォント '{font_name}' は見つかりませんでした。")

# QRコードを生成
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=3,
    border=0,
)
qr.add_data("https://efvock.github.io/music/enharmonic-chat")
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# 描画オブジェクトを作成
draw = ImageDraw.Draw(qr_img)

# フォントを指定
font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
# weight = "W6"
# font_path = get_font_path_by_name(font_name)
font_size = 16  # 適切なフォントサイズを設定
font = ImageFont.truetype(font_path, font_size)

# テキスト
text = "このページ自身"

# テキストのバウンディングボックスを取得
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# パディングを設定
padding_top = 10
padding_bottom = 10
padding_left = 10
padding_right = 10

# 背景用のバウンディングボックスを計算
background_bbox = (
    (qr_img.width - text_width) // 2 - padding_left,
    (qr_img.height - text_height) // 2 - padding_top,
    (qr_img.width + text_width) // 2 + padding_right,
    (qr_img.height + text_height) // 2 + padding_bottom,
)

# 背景の白い矩形を描画
draw.rectangle(background_bbox, fill="white")

# テキストを描画
text_position = (
    (qr_img.width - text_width) // 2,
    (qr_img.height - text_height) // 2,
)
draw.text(text_position, text, font=font, fill="black")

# 結果を保存または表示
qr_img.save("enharmonic-chat.qrcode.png")
