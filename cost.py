TXT = """\
保険料
    1,836,662
公共料金
    携帯電話
        263,346
医療費
    歯医者
        362,954
    RKS?
        428,124
    整形リハビリ
        538,724
クレジットカード
    888,275
"""


def main():
    from io import StringIO
    import re

    num_cre = re.compile(r"[\d,]+")

    g = StringIO(TXT)
    sum = 0
    for y in g:
        y = y.strip()
        if num_cre.match(y):
            y = int(y.replace(",", ""))
            sum += y

    print(f"{sum:,.0f} {sum / 24:,.0f}")


if __name__ == "__main__":
    main()
