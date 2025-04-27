#!/usr/bin/env python3

from json import dump, loads
from pathlib import Path

filename = Path("0.json")
json = filename.read_text()
o = loads(json)["page"]["entities"]
norm = {}
for k, v in o.items():
    norm[v["id"]] = v
with filename.with_suffix(".norm.json").open("w") as oobj:
    dump(norm, oobj, indent="  ")
    oobj.write("\n")
