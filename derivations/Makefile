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
# Section references (section(..., script="<label>")) resolve through the
# script outline ../slides/build/script-outline.json, regenerated here by
# ../scripts/script-outline.sh whenever a Typst source is newer; an exported
# copy without the script ships script-outline.json instead.
#
# Requirements: python3 with sympy and matplotlib (pytest for `make test`),
# latexmk for `make pdf`.

PYTHON  ?= python3
CHAPTERS := $(sort $(wildcard chapters/ch*.py))
NAMES    := $(notdir $(CHAPTERS:.py=))
TEX      := $(NAMES:%=build/tex/%.tex)
PDF      := $(NAMES:%=build/pdf/%.pdf)
# An exported copy without ../src uses the script-outline.json shipped with it.
OUTLINE  := $(if $(wildcard ../src),../slides/build/script-outline.json,script-outline.json)
TYPST    := $(if $(wildcard ../src),$(shell find ../src -name '*.typ'))

.PHONY: all test tex fig pdf outline clean
all: pdf

outline: $(OUTLINE)
ifneq ($(wildcard ../src),)
$(OUTLINE): $(TYPST) ../scripts/script-outline.sh
	bash ../scripts/script-outline.sh $@
endif

test: $(OUTLINE)
	$(PYTHON) -m pytest -q test_chapters.py

tex: $(TEX)
fig: $(TEX) build/fig/saha_cmod.svg
pdf: $(PDF)

build/tex/%.tex: chapters/%.py si.py notebook.py $(OUTLINE)
	PYTHONPATH=. $(PYTHON) $<

build/fig/saha_cmod.svg: plot_saha_cmod.py data/saha-cmod/data.csv
	$(PYTHON) plot_saha_cmod.py

build/pdf/%.pdf: build/tex/%.tex
	latexmk -pdf -quiet -interaction=nonstopmode -outdir=build/pdf $< >/dev/null
	latexmk -c -outdir=build/pdf $< >/dev/null

clean:
	rm -rf build
