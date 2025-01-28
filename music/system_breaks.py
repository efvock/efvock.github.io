#!/usr/bin/env python3

import xml.etree.ElementTree as ET


def insert_system_breaks(input_file, output_file):
    # MusicXML ファイルを読み込む
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 小節（<measure>）要素を取得
    measures = root.findall(".//measure")

    # 3n+1 小節ごとに <print new-system="yes"/> を挿入
    for i, measure in enumerate(measures):
        if (i + 1) % 3 == 1:  # 3n+1 条件
            print_tag = ET.Element("print")
            print_tag.set("new-system", "yes")
            measure.insert(0, print_tag)

    # 修正した MusicXML を保存
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"System breaks added and saved to {output_file}")


# 使用例
input_musicxml = "music/enharmonic.musicxml"  # 入力ファイル名
output_musicxml = "music/enharmonic.musicxml"  # 出力ファイル名
insert_system_breaks(input_musicxml, output_musicxml)
