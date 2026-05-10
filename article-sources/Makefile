TEMPLATE := template/pandoc.typ
ARTICLES  := $(wildcard */article.md)
PDFS      := $(ARTICLES:%.md=%.pdf)

.PHONY: all clean

all: $(PDFS)

# Convert article.md → article.pdf via pandoc (md→typst) + typst compile
%/article.pdf: %/article.md $(TEMPLATE)
	pandoc $< \
	  --template $(TEMPLATE) \
	  --to typst \
	  --output $*/_article_tmp.typ
	typst compile $*/_article_tmp.typ $@ --root .
	rm $*/_article_tmp.typ

clean:
	rm -f $(PDFS) */_article_tmp.typ
