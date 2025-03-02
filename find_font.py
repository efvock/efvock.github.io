#!/usr/bin/env python3

from PIL import ImageFont
from pathlib import Path
from json import load as load_json
from re import compile as cre


def find_font(pat, size):
    try:
        spat = pat.pattern
    except AttributeError:
        from re import compile as cre

        spat = pat
        pat = cre(spat)
    json = Path("~/.matplotlib/fontlist-v390.json").expanduser()
    obj = load_json(json.open())
    for k, v in obj.items():
        if not k.endswith("list"):
            continue
        if not v.__class__ is list:
            continue
        for vv in v:
            font_path = vv["fname"]
            if not pat.match(Path(font_path).name):
                continue
            return ImageFont.truetype(font_path, size)
    raise ValueError(f"{spat}: no such font")
