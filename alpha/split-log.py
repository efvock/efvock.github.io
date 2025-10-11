#!/usr/bin/env python3

from pathlib import Path
import re

DAY = re.compile(r"^(\d\d\d\d\.\d\d)\.(\d\d) (.)曜日")
DOW = dict(日="Sun", 月="Mon", 火="Tue", 水="Wed", 木="Thu", 金="Fri", 土="Sat")


def split(first_line, iobj):
    from null_context import NULL_CONTEXT

    m = DAY.search(first_line)
    if m is None:
        return None
    mm, dd, dow = (m.group(y + 1) for y in range(3))
    dow = DOW[dow]
    filename = Path(f"{mm}.{dd}.{dow}")
    if ("alpha-log" / filename).exists():
        filename = NULL_CONTEXT
    else:
        mm = mm.replace(".", "-")
        grouped = Path("alpha-log", mm, filename)
        if grouped.exists():
            filename = NULL_CONTEXT
        else:
            filename = "alpha-log" / filename
    with filename.open("w") as oobj:
        oobj.write(first_line)
        for y in iobj:
            m = DAY.search(y)
            if m:
                return y
            y = y.replace(" 堀内寛己 ", " <z ").replace(" あゆり ", " f> ")
            oobj.write(y)
        return y
    assert False


def skip(iobj):
    for y in iobj:
        if DAY.search(y):
            return y
    assert False


def main():
    with Path(__file__).with_name("ayuri.txt").open() as iobj:
        first_line = skip(iobj)
        while True:
            l = split(first_line, iobj)
            if l is None:
                break
            first_line = l


if __name__ == "__main__":
    main()
