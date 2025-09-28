#!/usr/bin/env/python3

from pathlib import Path
from dateutil import parser
import csv

LARGE_SCHEMA = "Order Date", "Total Owed", "Product Name"
SMALL_SCHEMA_KEN = dict(date="利用日", amount="支払総額", shop="利用店名・商品名")
DOWNLOADS = Path("~/Downloads").expanduser()
KEN = DOWNLOADS / "Your Orders"
H2 = DOWNLOADS / "Your Orders (1)"
LARGE_LOG_SUFFIX = "Retail.OrderHistory.3/Retail.OrderHistory.3.csv"
LARGE_LOG_PREFIX = dict(ken=KEN, h2=H2)


def large_log(whose):
    return LARGE_LOG_PREFIX[whose] / LARGE_LOG_SUFFIX


def simplify_date(date_string):
    return parser.parse(date_string).strftime("%Y-%m-%d")


def date_range(small_log, schema):
    with small_log.open() as iobj:
        rdr = csv.reader(iobj)
        firstline = rdr.__next__()
        rows = []
        for row_en in "date", "amount", "shop":
            row_label = schema[row_en]
            rows.append(firstline.index(row_label))
        amazon = 0
        for row in rdr:
            shop = row[rows[2]].strip().lower()
            date_string = row[rows[0]]
            if shop == "amazon.co.jp":
                yield [date_string, row[rows[1]], amazon]
                amazon += 1
            else:
                yield date_string, row[rows[1]], row[rows[2]]


def large_subset(whose, start, end):
    large = large_log(whose)
    with large.open() as iobj:
        rdr = csv.reader(iobj)
        firstline = rdr.__next__()
        date_index = firstline.index(LARGE_SCHEMA[0])
        amount_index = firstline.index(LARGE_SCHEMA[1])
        product_index = firstline.index(LARGE_SCHEMA[2])
        for row in rdr:
            date = row[date_index]
            date = simplify_date(date)
            if end < date:
                continue
            if date < start:
                break
            yield row[product_index]


def main():
    from datetime import timedelta

    one_day = timedelta(days=1)
    dates = tuple(date_range(DOWNLOADS / "enavi.csv", SMALL_SCHEMA_KEN))
    if not dates:
        return
    end, start = dates[0], dates[-1]
    start, end = (parser.parse(y[0]) - one_day for y in (start, end))
    start, end = (y.strftime("%Y-%m-%d") for y in (start, end))
    amazon = tuple(large_subset("ken", start, end))
    for row in dates:
        if row[2].__class__ is int:
            row[2] = f"amz {amazon[row[2]]}"
    pass


if __name__ == "__main__":
    main()
