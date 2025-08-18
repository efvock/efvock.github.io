#!/usr/bin/env python3


def main():
    from pathlib import Path
    from gdrive_put import gdrive_put_ex, gdrive_put_service
    src = Path(__file__).resolve().parent.with_name("mcorp-and-k")
    service = gdrive_put_service()
    g = []
    titles = []
    for y in sorted(src.glob("*.md")):
        if y.name != "index.md":
            t = title(y)
            titles.append(t)
            g.append(["null.docx", t])
    g = gdrive_put_ex(service, g)
    for y, t in zip(g, titles):
        yx = y.index("/edit")
        y = y[:yx] + "/edit"
        print(f"[{t}]({y})")


def title(filename):
    with filename.open() as g:
        g.__next__()
        l = g.__next__()
        l = l.strip()
        return l[7:]


if __name__ == "__main__":
    main()
