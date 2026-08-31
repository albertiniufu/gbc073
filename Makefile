# Extensões de arquivos temporários gerados pela compilação LaTeX (beamer)
clean:
	find . -type f \
		\( -name '*.aux' -o -name '*.log' -o -name '*.out' \
		 -o -name '*.toc' -o -name '*.nav' -o -name '*.snm' \
		 -o -name '*.vrb' -o -name '*.bbl' -o -name '*.blg' \
		 -o -name '*.fls' -o -name '*.fdb_latexmk' \
		 -o -name '*.synctex.gz' -o -name '*.xdv' -o -name '*.dvi' \) \
		-delete

# Recompila todas as aulas e relata linhas Overfull (padrão: zero)
AULAS = aula01 aula02 aula03 aula04 aula05 aula06 aula07 \
        aula08 aula09 aula10 aula11 aula12 aula13 aula14

verificar:
	@for d in $(AULAS) docs; do \
	  (cd $$d && latexmk -xelatex -interaction=nonstopmode *.tex >/dev/null 2>&1); \
	  n=$$(grep -i overfull $$d/*.log 2>/dev/null | wc -l); \
	  echo "$$d: $$n linha(s) Overfull"; \
	done

.PHONY: clean verificar
