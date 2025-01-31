#!/usr/bin/env python3

import xml.etree.ElementTree as ET


def insert_system_breaks(musicxml):
    # MusicXML ファイルを読み込む
    tree = ET.parse(musicxml)
    root = tree.getroot()

    # 小節（<measure>）要素を取得
    measures = root.findall(".//measure")

    # 3n+1 小節ごとに <print new-system="yes"/> を挿入
    for i, measure in enumerate(measures):
        if (i + 1) % 4 == 1:  # 4n+1 条件
            print_tag = ET.Element("print")
            print_tag.set("new-system", "yes")
            measure.insert(0, print_tag)

    # 修正した MusicXML を保存
    tree.write(musicxml, encoding="utf-8", xml_declaration=True)


from sys import argv

for musicxml in argv[1:]:
    insert_system_breaks(musicxml)
