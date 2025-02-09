all:

@@.mscz		:=$(wildcard *.mscz)

@@.music	:=$(@@.mscz:%.mscz=%.musicxml)
@@.xml		:=$(@@.mscz:%.mscz=%.xml)
@@.pdf		:=$(@@.mscz:%.mscz=%.pdf)
@@.png		:=$(@@.mscz:%.mscz=%.png)
@@.mp3		:=$(@@.mscz:%.mscz=%.mp3)
@@.export	:=$(@@.pdf) $(@@.png) $(@@.mp3)
@@.*		:=$(@@.music) $(@@.xml) $(@@.export)

$(@@.music)	:%.musicxml	:%.mscz
$(@@.xml)	:%.xml		:%.musicxml
$(@@.pdf)	:%.pdf		:%.mscz
$(@@.png)	:%.png		:%.mscz
$(@@.mp3)	:%.mp3		:%.mscz

define export
	open -a 'MuseScore 4' $<
	read -p 'done? '
endef

$(@@.music)	:
	$(export)
	../../system_breaks.py 4 $@

$(@@.png) \
$(@@.mp3)	:
	$(export)

$(@@.xml)	:%.xml		:%.musicxml
	cp $< $@

/chat	:=$(HOME)/Downloads/chat.pdf
//base	:=https://efvock.github.io/music/enharmonic
//chat	:=$(//base)/chat
//annex	:=$(//base)/annex

annex	:=annex.qrcode.png

$(/chat)	:chat.md $(annex)
	git add .
	git commit -a -m - || :
	git push || :
	open -na "Google Chrome" --args --incognito $(//chat)
	read -p 'done? '

chat.pdf	:$(/chat)
	cp $(/chat) $@

$(annex)	:
		../../qr.py $(//annex) annex

all		:$(@@.*) $(@@.pdf) chat.pdf

clean		:
	rm -f *.xml *.musicxml *.pdf
