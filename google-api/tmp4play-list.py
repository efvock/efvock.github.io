#!/usr/bin/env python3


def main():
    from gdrive_put import gdrive_put_ex, gdrive_put_service
    from pathlib import Path

    service = gdrive_put_service()
    g = (
        "風のゆくえ",
        "すこし風の日",
        "children's ballad",
        "gran's wisdom",
        "your tear",
        "recollections",
        "Celeste",
        "calm tempest",
        "out of accord",
        "blossoms",
        "bright eyes",
    )
    g2 = g.__iter__()
    there = Path("~/Downloads").expanduser()
    g = ([there / f"{short}.mp3", short] for short in g)

    for num, url in enumerate(gdrive_put_ex(service, g), 1):
        ix = url.index("/view?usp=drivesdk")
        url = url[:ix]
        url = f"{url}/preview"
        iframe = f'<iframe src="{url}" width="100%" allow="autoplay"></iframe>'
        print("<br/><br/>\n")
        print(f"## {num}. {g2.__next__()}\n")
        print(f"{iframe}\n")


if __name__ == "__main__":
    main()
