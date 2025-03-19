#!/bin/sh
pandoc --pdf-engine=xelatex --highlight-style zenburn --toc -N -H head.tex --from=markdown+pipe_tables main.md -o output.pdf
