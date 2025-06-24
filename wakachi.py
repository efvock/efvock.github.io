#!/usr/bin/env python3

import re

sss = """\
> KO 大学工学部機械工学科時代、K は、新聞にパラパラと「石油化学」という文字が出てくるのを見ていて、日頃から「何だろう?」と思っていた。
> その折りも折り、M社研究グループ編**石油化学工業**という本が出た。
> それを読んで、「これは面白い! 時代の最先端だ!!」と思った。
> そして信頼する先輩に「石油化学工業で機械屋の出番はあるだろうか?」と聞き「化学工場は機械の塊だ。もちろん出番は沢山ある」と聞き、人生の進路を決めた。
> M社には新卒第一期生として入社した。
"""

sss = "**『石油化学工業』**という本が出版された。"


def main():
    s = wakachi(sss)
    return
    from io import StringIO
    from sys import argv
    from pathlib import Path
    for y in argv[1:]:
        b = StringIO()
        y = Path(y)
        for yy in y.open("r"):
            s = wakachi(yy)
            b.write(s)
        y.write_text(b.getvalue())


ja = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
en = r'[\x20-\xff]'
jpunct = r'[\u3000-\u303F\u30FB]'
epunct = r'[!-/:-@[-`{-~]'
epunct = r'[!?.,]'
sp = r'\s*'
j2e = re.compile(f'({ja}){sp}({en})')
e2j = re.compile(f'({en}){sp}({ja})')
p2e = re.compile(f"({jpunct}) ({en})")
e2p = re.compile(f"({en}) ({jpunct})")
p2j = re.compile(f"({epunct}) ({ja})")
j2p = re.compile(f"({ja}) ({epunct})")
gap = re.compile(f">({jpunct})")
# em_ee = re.compile(f"({en}) \* ({en})")
# em_ej = re.compile(f"({en}) \* ({ja})")
# em_je = re.compile(f"({ja}) \* ({en})")
# em_jj = re.compile(f"({ja}) \* ({ja})")
strong_ee = re.compile(f"({en}) \*\* ({en})")
strong_ej = re.compile(f"({en}) \*\* ({ja})")
strong_je = re.compile(f"({ja}) \*\* ({en})")
strong_jj = re.compile(f"({ja}) \*\* ({ja})")


def wakachi(s):
    s = j2e.sub(r"\1 \2", s)
    s = e2j.sub(r"\1 \2", s)
    s = p2e.sub(r"\1\2", s)
    s = e2p.sub(r"\1\2", s)
    # s = p2j.sub(r"\1\2", s)
    s = j2p.sub(r"\1\2", s)
    s = strong_jj.sub(r"\1**\2", s)
    s = gap.sub(r"> \1", s)
    return s


# print(wakachi("aあ"))
# print(wakachi("あb"))
# print(wakachi("aあb"))
# print(wakachi("a「b」c"))
# print(wakachi("a 「 b 」 c"))
# print(wakachi("a、b"))
# print(wakachi("a 、b"))

if __name__ == "__main__":
    main()
