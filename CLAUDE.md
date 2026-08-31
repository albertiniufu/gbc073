# GBC073 — Inteligência Computacional (regras do projeto)

## Restrição de frameworks

Todo código, exemplo e menção instrutiva nos materiais do curso usa
**PyTorch** (`torch`, `torch.nn`). **Nunca** adicionar conteúdo, código ou
exemplos de **Keras/TensorFlow** (`tf.keras`, `tensorflow.*`).

- Em materiais adaptados que tragam trechos de Keras/TensorFlow, portar o
  trecho para PyTorch ou omiti-lo por completo — nunca mantê-lo lado a lado.
- A regra vale para slides, handouts, simuladores e notas.

## Compilação

- **XeLaTeX obrigatório** (o tema carrega `fontspec`; `pdflatex` não funciona),
  **duas passadas** (a barra de progresso do rodapé depende da segunda).
- O tema (`beamerthemeInteligenciaComputacional.sty`) e o estilo de handout
  ficam na raiz; cada `.tex` resolve com o truque `\input@path{{./}{../}}`.
- Ordem de carregamento: `\usetheme` (ou o `.sty` do handout) ANTES de `babel`.
- Padrão **zero Overfull**: `xelatex -interaction=nonstopmode aula.tex | grep Overfull`.

## Convenções de conteúdo

- Usar caixas, macros e paleta do tema ic — consultar `docs/GUIA-DO-TEMPLATE-GBC073.md`.
- Português; convenções de tradução na seção 11 do guia do template.
- Cada aula registra no cabeçalho do `.tex` o mapeamento com a ementa
  (ficha SEI 5116656).
- Material de terceiros que exige atribuição (ex.: MIT 6.S191) deve ser
  citado no cabeçalho e no frame de referências da aula.
