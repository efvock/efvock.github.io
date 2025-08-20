#!/usr/bin/env python3


def main():
    from gdrive_put import gdrive_put_ex, gdrive_put_service
    from pathlib import Path

    service = gdrive_put_service()
    g = (
        ["third-wind.mp3", "Third Wind"],
        ["beat70.mp3", "Beat 70"],
        ["better-days-ahead.mp3", "Better Days Ahead"],
        ["first-circle.mp3", "First Circle"],
        ["bilbao.mp3", "Song for Bilbao"],
        ["straight-on-red.mp3", "Straight on Red"],
    )
    g2 = (long for _, long in g)
    dwhelper = Path("~/dwhelper").expanduser()
    g = ([dwhelper / short, short] for short, _ in g)

    for num, url in enumerate(gdrive_put_ex(service, g), 10):
        ix = url.index("/view?usp=drivesdk")
        url = url[:ix]
        url = f"{url}/preview"
        iframe = f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>'
        print("<br/><br/>\n")
        print(f"## {num}. {g2.__next__()}\n")
        print(f"{iframe}\n")


if __name__ == "__main__":
    main()
