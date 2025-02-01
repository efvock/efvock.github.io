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

//chat	:=https://efvock.github.io/music/enharmonic/chat
/chat	:=$(HOME)/Downloads/chat.pdf

$(/chat)	:chat.md
	open -na "Google Chrome" --args --incognito $(//chat)
	read -p 'done? '

chat.pdf	:$(/chat)
	cp $(/chat) $@

all			:	$(@@.*) so.pdf chat.pdf

clean		:
	rm -f *.xml *.png *.mp3 *.pdf
