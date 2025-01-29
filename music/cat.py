#!/usr/bin/env python3

from music21 import converter, stream

# 2つの MusicXML ファイルを読み込む
score1 = converter.parse("enharmonic.musicxml")
score2 = converter.parse("double-sharp.musicxml")

# スコアを連結する
merged_score = stream.Score()
merged_score.append(score1)
merged_score.append(score2)

# 新しい MusicXML ファイルとして保存
merged_score.write("musicxml", "cat.musicxml")
