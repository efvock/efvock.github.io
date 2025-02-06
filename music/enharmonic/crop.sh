ffmpeg -i fa.mov -vf 'crop=844:805:(iw-844):(ih-805)' -c:v prores -profile:v 3 fa-crop.mov
