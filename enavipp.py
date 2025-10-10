#!/usr/bin/env python3

from pathlib import Path
import csv

INTERESTED = "利用日", "利用店名・商品名", "支払総額"
ENAVI = Path(f"~/Downloads/enavi.csv").expanduser()
ENAVI_A = ENAVI.with_suffix(".a.csv")
ENAVI_B = ENAVI.with_suffix(".b.csv")
ENAVI_C = ENAVI.with_suffix(".c.csv")


def unbom():
    txt = ENAVI.read_bytes()
    if txt[:3] == b"\xef\xbb\xbf":
        txt = txt[3:]
    ENAVI_A.write_bytes(txt)


def interested_columns():
    yield 0
    with ENAVI_A.open() as iobj:
        header = csv.reader(iobj).__next__()
        for y in INTERESTED:
            interested = header.index(y)
            yield interested + 1


def add_amazon_column():
    with ENAVI_A.open() as iobj, ENAVI_B.open("w") as oobj:
        rdr = csv.reader(iobj)
        wtr = csv.writer(oobj)
        for row in rdr:
            wtr.writerow([0] + row)


def squeeze(row):
    interested = tuple(interested_columns())
    return [row[column] for column in interested]


def main():
    from operator import itemgetter

    unbom()
    with ENAVI_B.open() as iobj, ENAVI_C.open("w") as oobj:
        add_amazon_column()
        rdr = csv.reader(iobj)
        wtr = csv.writer(oobj)
        data = [squeeze(y) for y in rdr]
        data[0][0] = "amazon"
        data[1:] = sorted(data[1:], reverse=True)
        for row in data[1:]:
            row[0] = int(row[2] == "AMAZON.CO.JP")
        wtr.writerows(data)


if __name__ == "__main__":
    main()
