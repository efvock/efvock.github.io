#!/usr/bin/env/python3


INTERESTED = (
    "Order Date",
    "Total Owed",
    "Product Name"
)


def annotate(infile, outfile):
    from pathlib import Path
    import csv
    filename = Path(filename)