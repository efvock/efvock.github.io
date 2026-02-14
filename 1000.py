#!/usr/bin/env python3


def main():
    from pathlib import Path

    path = Path("scrap-master.md")
    print(path.read_text()[1000:])


if __name__ == "__main__":
    main()
