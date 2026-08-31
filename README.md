# GBC073 — Inteligência Computacional

Materiais da disciplina **GBC073 — Inteligência Computacional** (UFU/FACOM): slides, simuladores interativos que rodam no navegador e, em breve, resumos (handouts). O curso percorre os três paradigmas da inteligência computacional na aula introdutória e aprofunda, nas 13 aulas seguintes, a parte que a história escolheu: redes neurais e deep learning.

**Pergunta do curso:** "Como construir máquinas que aprendem a partir de dados?"

## Aulas

| Aula | Slides | Resumo | Simulador | Extras |
|------|--------|--------|-----------|--------|
| 1 — Introdução: redes neurais como aproximadores universais | [PDF](aula01/aula01.pdf) | — | [Perceptron](https://albertiniufu.github.io/gbc073/aula01/simulador-perceptron.html) | — |
| 2 — O que uma rede consegue representar | [PDF](aula02/aula02.pdf) | — | [Representatividade](https://albertiniufu.github.io/gbc073/aula02/aula02-simulador-representatividade.html) | — |
| 3 — Aprendendo a rede — Parte 1 | [PDF](aula03/aula03.pdf) | — | [Lab](https://albertiniufu.github.io/gbc073/aula03/aula03-lab.html) | — |
| 4 — Aprendendo a rede — Parte 2: retropropagação | [PDF](aula04/aula04.pdf) | — | — | — |
| 5 — Treinar é otimizar: descida de gradiente e suas variações | [PDF](aula05/aula05.pdf) | — | — | — |
| 6 — A rede que decora: sobreajuste, regularização e generalização | [PDF](aula06/aula06.pdf) | — | — | — |
| 7 — Redes que enxergam: convolução | [PDF](aula07/aula07.pdf) | — | — | — |
| 8 — Redes que leem: sequências, recorrência e memória | [PDF](aula08/aula08.pdf) | — | — | — |
| 9 — Atenção: quando a rede aprende onde olhar | [PDF](aula09/aula09.pdf) | — | — | — |
| 10 — Aprender sem professor: autoencoders e embeddings | [PDF](aula10/aula10.pdf) | — | — | — |
| 11 — Memória e mapas: Hopfield, Kohonen e aprendizado hebbiano | [PDF](aula11/aula11.pdf) | — | — | — |
| 12 — Aplicações: interpolação e campos neurais | [PDF](aula12/aula12.pdf) | — | — | — |
| 13 — Aplicações: classificação em escala e projeto de redes | [PDF](aula13/aula13.pdf) | — | — | — |
| 14 — Encerramento: o mapa da inteligência computacional | [PDF](aula14/aula14.pdf) | — | — | — |

## Como compilar

- Os slides usam **XeLaTeX** (o tema carrega `fontspec`; `pdflatex` não funciona).
- São necessárias **duas passadas** — a barra de progresso do rodapé depende da segunda.
- O tema (`beamerthemeInteligenciaComputacional.sty`) e o estilo de handout
  (`handoutInteligenciaComputacional.sty`) ficam na raiz e são resolvidos pelo
  truque `\input@path{{./}{../}}` em cada `.tex`.

```bash
latexmk -xelatex aula01/aula01.tex    # recomendado (dentro da pasta da aula)
make clean                            # remove os arquivos temporários do LaTeX
make verificar                        # recompila tudo e lista linhas Overfull
```

No Overleaf: *Settings → Compiler → XeLaTeX*.

## Licença

[CC0 1.0 Universal](LICENSE) — domínio público.
