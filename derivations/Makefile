# SymPy derivations for the plasma-physics script.
#
#   make test   check every derivation against the formula printed in the script
#   make tex    run each chapter file; writes build/tex/<chapter>.tex and the
#               plots of derived results to build/fig/<name>.{svg,pdf}
#   make fig    same as make tex (plots and LaTeX come from one run)
#   make pdf    compile the LaTeX files to build/pdf/<chapter>.pdf
#   make        tex + pdf
#   make clean  remove build/
#
# Requirements: python3 with sympy and matplotlib (pytest for `make test`),
# latexmk for `make pdf`.

PYTHON  ?= python3
CHAPTERS := $(sort $(wildcard chapters/ch*.py))
NAMES    := $(notdir $(CHAPTERS:.py=))
TEX      := $(NAMES:%=build/tex/%.tex)
PDF      := $(NAMES:%=build/pdf/%.pdf)

.PHONY: all test tex fig pdf clean
all: pdf

test:
	$(PYTHON) -m pytest -q chapters

tex: $(TEX)
fig: $(TEX)
pdf: $(PDF)

build/tex/%.tex: chapters/%.py si.py
	PYTHONPATH=. $(PYTHON) $<

build/pdf/%.pdf: build/tex/%.tex
	latexmk -pdf -quiet -interaction=nonstopmode -outdir=build/pdf $< >/dev/null
	latexmk -c -outdir=build/pdf $< >/dev/null

clean:
	rm -rf build
