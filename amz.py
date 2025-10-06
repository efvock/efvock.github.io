#!/usr/bin/env/python3

from pathlib import Path
from dateutil import parser
import csv

LARGE_SCHEMA = dict(
    date="Order Date",
    amount="Total Owed",
    product="Product Name",
)
SMALL_SCHEMA_KEN = dict(
    date="利用日",
    amount="支払総額",
    shop="利用店名・商品名",
)
DOWNLOADS = Path("~/Downloads").expanduser()
KEN = DOWNLOADS / "Your Orders"
H2 = DOWNLOADS / "Your Orders (1)"
LARGE_LOG_SUFFIX = "Retail.OrderHistory.3/Retail.OrderHistory.3.csv"
LARGE_LOG_PREFIX = dict(ken=KEN, h2=H2)


def large_log(whose):
    return LARGE_LOG_PREFIX[whose] / LARGE_LOG_SUFFIX


def simplify_date(date_string):
    return parser.parse(date_string).strftime("%Y-%m-%d")


def columns_logical(rdr, **schema):
    columns_physical = rdr.__next__()
    columns = []
    for column_en in schema.keys():
        column_label = schema[column_en]
        columns.append(columns_physical.index(column_label))
    return columns


def enavi_range(small_log, **schema):
    with small_log.open() as iobj:
        rdr = csv.reader(iobj)
        columns = columns_logical(rdr, **schema)
        amazon = 0
        date_x, amount_x, shop_x = columns[0], columns[1], columns[2]
        for row in rdr:
            shop = row[shop_x].strip().lower()
            date_string = row[date_x]
            sort_key = f"{date_string}/{shop}"
            if shop == "amazon.co.jp":
                yield [date_string, row[amount_x], amazon, sort_key]
                amazon += 1
            else:
                yield [date_string, row[amount_x], row[shop_x], sort_key]


def amazon_summary(whose, start, end):
    large = large_log(whose)
    with large.open() as iobj:
        rdr = csv.reader(iobj)
        columns = columns_logical(rdr, **LARGE_SCHEMA)
        date_x, amount_x, product_x = columns[0], columns[1], columns[2]
        for row in rdr:
            date = row[date_x]
            date = simplify_date(date)
            if end < date:
                continue
            if date < start:
                break
            yield row[amount_x].replace(",", ""), row[product_x]


def main():
    from datetime import timedelta
    from itertools import groupby, permutations
    from operator import itemgetter

    one_day = timedelta(days=1)
    enavi = tuple(enavi_range(DOWNLOADS / "enavi.csv", **SMALL_SCHEMA_KEN))
    if not enavi:
        return
    yield list(SMALL_SCHEMA_KEN.values())
    end, start = enavi[0], enavi[-1]
    start, end = (parser.parse(y[0]) - one_day for y in (start, end))
    start, end = (y.strftime("%Y-%m-%d") for y in (start, end))
    amazon = tuple(amazon_summary("ken", start, end))
    split = {}
    for k, v in groupby(enavi, itemgetter(3)):
        split[k] = list(v)
    for k, v in split.items():
        assert v
        if v[0][2].__class__ == str:
            continue
        permu = permutations(y[1] for y in v)
        ok = False
        for p in permu:
            nok = 0
            for vv, pp in zip(v, p):
                vv[1] = pp
                amazon_row = amazon[vv[2]]
                if pp == amazon_row[0]:
                    nok += 1
            if nok == p.__len__():
                ok = True
                break
        assert ok
    for row in enavi:
        shop = row[2]
        if shop.__class__ is int:
            row[2] = f"amz {amazon[shop][1]}"
        yield row[:3]


if __name__ == "__main__":
    import csv
    from sys import stdout

    wtr = csv.writer(stdout)
    for row in main():
        wtr.writerow(row)
    pass