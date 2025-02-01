all:

@@.mscz		:=$(wildcard *.mscz)
@@.music	:=$(@@.mscz:%.mscz=%.musicxml)
@@.xml		:=$(@@.mscz:%.mscz=%.xml)
@@.png		:=$(@@.mscz:%.mscz=%.png)
@@.mp3		:=$(@@.mscz:%.mscz=%.mp3)
@@.pdf		:=$(@@.mscz:%.mscz=%.pdf)
@@.export	:=$(@@.png) $(@@.mp3)
@@.*		:=$(@@.music) $(@@.export) $(@@.xml) so.pdf

define export
	open -a 'MuseScore 4' $<
	read -p 'done? '
endef

$(@@.music)	:%.musicxml	:%.mscz
$(@@.xml)	:%.xml		:%.musicxml
$(@@.png)	:%.png		:%.mscz
$(@@.mp3)	:%.mp3		:%.mscz
$(@@.pdf)	:%.pdf		:%.mscz

$(@@.music):
	$(export)
	../../system_breaks.py $@

$(@@.png) $(@@.mp3) $(@@.pdf):
	$(export)

$(@@.xml)	:%.xml		:%.musicxml
	cp $< $@

chat.pdf:	chat.md
	open https://efvock.github.io/music/enharmonic/chat
	read -p 'done? '

all:	$(@@.*) so.pdf chat.pdf
