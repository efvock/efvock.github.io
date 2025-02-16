#!/usr/bin/env python3

import xml.etree.ElementTree as ET


def insert_system_breaks(n, musicxml):
    # MusicXML ファイルを読み込む
    tree = ET.parse(musicxml)
    root = tree.getroot()

    # 小節（<measure>）要素を取得
    measures = root.findall(".//measure")

    for i, measure in enumerate(measures):
        if (i + 1) % n == 1:
            print_tag = ET.Element("print")
            print_tag.set("new-system", "yes")
            measure.insert(0, print_tag)

    # 修正した MusicXML を保存
    tree.write(musicxml, encoding="utf-8", xml_declaration=True)


from sys import argv

n = int(argv[1])
for musicxml in argv[2:]:
    insert_system_breaks(n, musicxml)
