#!/usr/bin/env python3

from json import dumps, loads
from pathlib import Path
import re

video_cre = re.compile(r'.*<iframe\s+src="(.*?)".*')
headline_cre = re.compile(r"<.*?>(.*?)<.*>")

from xids import ids
from xscripts import extract_scripts

html = Path("train-mix-voice.html").read_text()

html_attr_ids = tuple(ids(html))

script = extract_scripts(html).__next__()
script = loads(script)
script = script["page"]["entities"]

Path("1.json").write_text(
    dumps(script, indent="  ") + "\n"
)

map = {}
for k, v in script.items():
    try:
        map[v["htmlAttrId"]] = k
    except KeyError:
        pass

ordered = {}
for k in html_attr_ids:
    try:
        ordered[k] = script[map[k]]
    except KeyError:
        pass


def get_children(v):
    try:
        childids = v["childIds"]
    except KeyError:
        pass
    else:
        for k in childids:
            yield k
            yield from get_children(script[k])


for v in ordered.values():
    map = {}
    for kk in get_children(v):
        vv = script[kk]
        html_attr_id = vv["htmlAttrId"]
        spl = html_attr_id.split("-")
        map[spl[0]] = vv
    if "video" not in map or "headline" not in map:
        continue
    video = map["video"]["embedCode"]
    video = video_cre.match(video).group(1)
    print(video)
    headline = map["headline"]["html"]
    headline = headline_cre.match(headline).group(1)
    print(headline)
