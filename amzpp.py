AMAZON_CSV = "Retail.OrderHistory.3/Retail.OrderHistory.3.csv"

from pathlib import Path
import csv
import re

INTERESTED = "Ship Date", "Total Owed", "Product Name"


def copy(zipfile, csvfile):
    from tempfile import TemporaryDirectory
    from shutil import copy
    from subprocess import run

    suffixes = (f".{y}.csv" for y in "abc")
    csv_a, csv_b, csv_c = (csvfile.with_suffix(y) for y in suffixes)

    with TemporaryDirectory() as tmp:
        run(["unzip", "-q", Path(zipfile).absolute()], cwd=tmp)
        txt_a = Path(tmp, AMAZON_CSV).read_bytes()
    csv_a.write_bytes(txt_a)

    if txt_a[:3] == b"\xef\xbb\xbf":
        txt_b = txt_a[3:]
    else:
        txt_b = txt_a
    csv_b.write_bytes(txt_b)


def interested_rows(csvfile):
    with csvfile.open() as iobj:
        header = csv.reader(iobj).__next__()
        for y in INTERESTED:
            yield header.index(y)


def squeeze(csvfile):
    import csv

    interested = tuple(interested_rows(csvfile))
    with csvfile.open() as iobj:
        rdr = csv.reader(iobj)
        for row in rdr:
            yield [row[y] for y in interested]


AND_RE = r"(.+)\s+and\s+(.+)"
AND_CRE = re.compile(AND_RE)

def exclude_invalid_date(g):
    from dateutil import parser

    for y in g:
        y0 = y[0]
        m = AND_CRE.search(y0)
        if m:
            y0a = m.group(1)
            y0b = m.group(1)
            parser.parse(y0a)
            parser.parse(y0b)
            y[0] = y0a
            yield y
        else:
            try:
                parser.parse(y0)
            except:
                ok = False
            else:
                ok = True
            if y0 == "Not Available":
                continue
            if y0.startswith("Due to technical limitations"):
                continue
            if ok:
                yield y
            else:
                pass


WHOSE = dict(h2="Your Orders (1).zip", ken="Your Orders.zip")


def main():
    from operator import itemgetter
    for user, zipfile in WHOSE.items():
        csvfile = Path(f"amz-{user}.csv")
        copy(Path(f"~/Downloads/{zipfile}").expanduser(), csvfile)
        squeezed = list(squeeze(csvfile.with_suffix(".b.csv")))
        data = list(exclude_invalid_date(squeezed[1:]))
        data.sort(key=itemgetter(0), reverse=True)
        with csvfile.with_suffix(".c.csv").open("w") as oobj:
            wtr = csv.writer(oobj)
            wtr.writerow(squeezed[0])
            wtr.writerows(data)


if __name__ == "__main__":
    main()
