<<	:=$(wildcard *.md)
@@	:=$(<<:%.md=%.html)
+	:$(@@)
$(@@):%.html:%.md
	pandoc $< -o $@
