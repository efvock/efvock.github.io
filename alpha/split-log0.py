#!/usr/bin/env python3

from pathlib import Path
import re

DAY = re.compile(r"^(\d\d\d\d)/(\d+)/(\d+)\((.)\)")
DOW = dict(日="Sun", 月="Mon", 火="Tue", 水="Wed", 木="Thu", 金="Fri", 土="Sat")


def split(first_line, iobj):
    from null_context import NULL_CONTEXT

    m = DAY.search(first_line)
    if m is None:
        return None
    year, month, day, dow = m.group(1), m.group(2), m.group(3), DOW[m.group(4)]
    if month.__len__() == 1:
        month = f"0{month}"
    if day.__len__() == 1:
        day = f"0{day}"
    filename = Path(f"alpha-log/{year}.{month}.{day}.{dow}")
    if filename.exists():
        filename = NULL_CONTEXT

    with filename.open("w") as oobj:
        oobj.write(first_line)
        for y in iobj:
            m = DAY.search(y)
            if m:
                return y
            y = y.replace("\t堀内寛己\t", " <z ").replace("\tあゆり\t", " f> ")
            oobj.write(y)
        return y
    return None


def skip(iobj):
    for y in iobj:
        if DAY.search(y):
            return y
    return None


def main():
    with Path(__file__).with_name("ayuri0.txt").open() as iobj:
        first_line = skip(iobj)
        while True:
            l = split(first_line, iobj)
            if l is None:
                break
            first_line = l


if __name__ == "__main__":
    main()
