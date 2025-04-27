#!/usr/bin/env python3


def main():
    from json import load
    from pathlib import Path

    seen = set()

    whole = load(Path("0.norm.json").open())

    def walk(k, indent):
        if k in seen:
            return
        seen.add(k)
        v = whole[k]
        t = v["type"]
        if t == "Video":
            name = v["embedCode"]
        elif t in ("Column", "Row", "Section"):
            name = v["htmlAttrId"]
        elif t == "Headline":
            name =v["html"]
        else:
            name = "?" + t
        print(indent + k, name)
        try:
            chids = v["childIds"]
        except:
            pass
        else:
            for kk in chids:
                walk(kk, "  " + indent)

    for k, v in  whole.items():
        if v["type"] == "Section":
            walk(k, "")

if __name__ == "__main__":
    main()
