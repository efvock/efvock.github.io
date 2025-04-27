#!/usr/bin/env python3

from pathlib import Path


def g(text):
    from re import finditer
    prefix = r"https://iframe\.mediadelivery\.net/embed/"
    pattern = prefix + r'[^\\]+'

    for match in finditer(pattern, text):
        yield match.group()

text = Path("train-mix-voice.html").read_text()

for y in g(text):
    print(y)
