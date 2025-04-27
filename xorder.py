#!/usr/bin/env python3

from json import dumps, loads
from pathlib import Path

from xids import ids
from xscripts import extract_scripts

html = Path("train-mix-voice.html").read_text()

html_attr_ids = tuple(ids(html))

script = extract_scripts(html).__next__()
script = loads(script)
script = script["page"]["entities"]

normal = {}
id2html_attr = {}
for v in script.values():
    try:
        html_attr = v["htmlAttrId"]
        normal[html_attr] = v
        id2html_attr[v["id"]] = html_attr
    except KeyError:
        pass


Path("1.json").write_text(
    dumps(normal, indent="  ") + "\n"
)


def get_children(v):
    try:
        childids = v["childIds"]
    except KeyError:
        pass
    else:
        for k in childids:
            html_attr = id2html_attr[k]
            yield html_attr
            yield from get_children(normal[html_attr])


for k, v in normal.items():
    children = tuple(get_children(v))
    map = {}
    for y in children:
        spl = y.split("-")
        map[spl[0]] = y
    if "video" in map and "headline" in map:
        video, headline = map["video"], map["headline"]
        video, headline = normal[video], normal[headline]
        print(video["embedCode"], headline["html"])
