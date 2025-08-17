#!/usr/bin/env python3


def null_docx():
    from os.path import devnull
    import pypandoc
    from gdrive_put import gdrive_put

    out = "null.docx"
    pypandoc.convert_file(source_file="null.gfm", to="docx", outputfile=out)


if __name__ == "__main__":
    null_docx()
