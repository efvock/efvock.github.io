#!/usr/bin/env python3


def main():
    from pathlib import Path
    import unicodedata

    path = Path("scrap-master.md")
    nfkc = unicodedata.normalize("NFKC", path.read_text())
    path.write_text(nfkc)


if __name__ == "__main__":
    main()
