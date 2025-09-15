#!/usr/bin/env python3

from pathlib import Path
import re

DAY = re.compile(r"^(\d\d\d\d\.\d\d\.\d\d) (.)曜日")
DOW = dict(日="Sun", 月="Mon", 火="Tue", 水="Wed", 木="Thu", 金="Fri", 土="Sat")


class Null:
    def __getattr__(self, *args, **kwargs):
        def wrap(*args, **kwargs):
            return self

        return wrap

    def __enter__(self):
        return self

    def __exit__(self, *_args, **_kwargs):
        pass


NULL = Null()


def split(first_line, iobj):
    m = DAY.search(first_line)
    if m is None:
        return None
    filename = Path(f"alpha-log/{m.group(1)}.{DOW[m.group(2)]}")
    if filename.exists():
        filename = NULL

    with filename.open("w") as oobj:
        oobj.write(first_line)
        for y in iobj:
            m = DAY.search(y)
            if m:
                return y
            y = y.replace(" 堀内寛己 ", " <z ").replace(" あゆり ", " f> ")
            oobj.write(y)
        return y
    return None


def skip(iobj):
    for y in iobj:
        if DAY.search(y):
            return y
    return None


def main():
    with Path("~/Downloads/ayuri.txt").expanduser().open() as iobj:
        first_line = skip(iobj)
        while True:
            l = split(first_line, iobj)
            if l is None:
                break
            first_line = l


if __name__ == "__main__":
    main()
