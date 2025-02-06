all:

@@.mscz		:=$(wildcard *.mscz)

@@.music	:=$(@@.mscz:%.mscz=%.musicxml)
@@.xml		:=$(@@.mscz:%.mscz=%.xml)
@@.pdf		:=$(@@.mscz:%.mscz=%.pdf)
@@.*		:=$(@@.music) $(@@.xml) $(@@.pdf)

$(@@.music)	:%.musicxml	:%.mscz
$(@@.xml)	:%.xml		:%.musicxml
$(@@.pdf)	:%.pdf		:%.mscz

$(@@.music)	:
	open -a 'MuseScore 4' $<
	read -p 'done? '
	../../system_breaks.py $@

$(@@.xml)	:%.xml		:%.musicxml
	cp $< $@

/chat	:=$(HOME)/Downloads/chat.pdf
//base	:=https://efvock.github.io/music/enharmonic
//chat	:=$(//base)/chat
//annex	:=$(//base)/annex

annex	:=annex.qrcode.png

$(/chat)	:chat.md $(annex)
	git add .
	git commit -a -m -
	git push
	open -na "Google Chrome" --args --incognito $(//chat)
	read -p 'done? '

chat.pdf	:$(/chat)
	cp $(/chat) $@

$(annex)	:
		../../qr.py $(//annex) annex

all		:$(@@.*) $(@@.pdf) chat.pdf

clean		:
	rm -f *.xml *.musicxml *.pdf
