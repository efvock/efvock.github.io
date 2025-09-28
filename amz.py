#!/usr/bin/env/python3

from pathlib import Path
from dateutil import parser
import pytz
import csv

LARGE_SCHEME = "Order Date", "Total Owed", "Product Name"
SHORT_SCHEME_KEN = dict(date="利用日", shop="利用店名・商品名", amount="支払総額")
DOWNLOADS = Path("~/Downloads").expanduser()
KEN = DOWNLOADS / "Your Orders"
H2 = DOWNLOADS / "Your Orders (1)"
LARGELOG = "Retail.OrderHistory.3/Retail.OrderHistory.3.csv"


def largelog(whose):
    return dict(ken=KEN, h2=H2)[whose] / LARGELOG

def simplify_date(date_string):
    return parser.parse(date_string).strftime("%Y-%m-%d")

def date_range(smalllog, scheme):
    with smalllog.open() as iobj:
        rdr = csv.reader(iobj)
        firstline = rdr.__next__()
        rows = []
        for row in "date", "shop", "amount":
            name = scheme[row]
            rows.append(firstline.index(name))
        for row in rdr:
            if row[1].strip().lower() == "amazon.co.jp":
                datestring = row[0]
                yield datestring


def large_subset(whose, start, end):
    large = largelog(whose)
    with large.open() as iobj:
        rdr = csv.reader(iobj)
        firstline = rdr.__next__()
        date_index = firstline.index(LARGE_SCHEME[0])
        amount_index = firstline.index(LARGE_SCHEME[1])
        product_index = firstline.index(LARGE_SCHEME[2])
        for row in rdr:
            date = row[date_index]
            date = simplify_date(date)
            if start <= date <= end:
                yield date, row[amount_index], row[product_index]

def main():
    from datetime import timedelta

    one_day = timedelta(days=1)
    dates = tuple(date_range(DOWNLOADS / "enavi.csv", SHORT_SCHEME_KEN))
    end, start = dates[0], dates[-1]
    start, end = (parser.parse(y) - one_day for y in (start, end))
    start, end = (y.strftime("%Y-%m-%d") for y in (start, end))
    large = tuple(large_subset("ken", start, end))
    pass


if __name__ == "__main__":
    main()
