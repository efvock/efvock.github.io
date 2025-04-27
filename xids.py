#!/usr/bin/env python3


def ids(html_text):
    from html.parser import HTMLParser

    rv = []

    class IDs(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr == "id":
                    rv.append(value)

    parser = IDs()
    parser.feed(html_text)
    return rv


if __name__ == "__main__":
    from pathlib import Path

    for y in ids(Path("train-mix-voice.html").read_text()):
        print(y)
