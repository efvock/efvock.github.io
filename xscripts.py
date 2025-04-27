#!/usr/bin/env python3

from html.parser import HTMLParser
from pathlib import Path


def main():
    html = Path("train-mix-voice.html").read_text()
    for i, script in enumerate(extract_scripts(html)):
        from json import dumps, loads
        o = loads(script)
        ser = dumps(o, indent="  ")
        Path(f"{i}.json").write_text(ser + "\n")


def extract_scripts(html_text):
    rv = []

    class ScriptExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_script = False

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "script":
                self.in_script = True

        def handle_endtag(self, tag):
            if tag.lower() == "script" and self.in_script:
                self.in_script = False

        def handle_data(self, data):
            if self.in_script:
                rv.append(data.replace(r"\x3c", r"\u003c"))
    
    parser = ScriptExtractor()
    parser.feed(html_text)

    for y in rv:
        if y.startswith("window.__PRELOADED_STATE__ = "):
            trim = 29
        elif y.startswith("window.initialI18nStore = "):
            trim = 26
        else:
            continue
        yield y[trim:]


if __name__ == "__main__":
    main()
