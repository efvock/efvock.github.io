#!/usr/bin/env python3

from sys import argv

mov, param = argv[1], int(argv[2])

if param == 0:
    x0, y0 = 329, 152
    x1, y1 = 1173, 957
else:
    x0, y0 = 336, 159
    x1, y1 = 1177, 962

x0 -= 30
x1 -= 30
w, h = x1-x0, y1-y0

print(f"rm -f {mov}-crop.mov")
hq = "-c:v prores -profile:v 3"
print(f"ffmpeg -i {mov}.mov -vf crop={w}:{h}:{x0}:{y0} {hq} {mov}-crop.mov")
