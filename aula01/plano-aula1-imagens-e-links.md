# Plano — Imagens e links complementares da Aula 1 (GBC073)

Objetivo: deixar a aula 1 mais visual e com material complementar por
assunto. Tudo vem de fontes livres (Wikimedia Commons / Wikipedia) com
licenças compatíveis com material didático; cada imagem tem autor e
licença registrados aqui e no script de download.

---

## 1. Imagens — o que entrou nos slides

| # | Slide | Arquivo local | Fonte (Commons) | Autor | Licença |
|---|-------|---------------|-----------------|-------|---------|
| 1 | O momento em que estamos | `nobel-2024.jpg` | [John J. Hopfield and Geoffrey E. Hinton, 2024 Nobel Prize Laureate in Physics](https://commons.wikimedia.org/wiki/File:John_J._Hopfield_and_Geoffrey_E._Hinton,_2024_Nobel_Prize_Laureate_in_Physics.jpg) | Arthur Petron | CC BY-SA 4.0 |
| 2 | 1958, em hardware: o Mark I Perceptron | `mark1.jpg` | [330-PSA-80-60 (USN 710739)](https://commons.wikimedia.org/wiki/File:330-PSA-80-60_(USN_710739)_(20897323365).jpg) | National Museum of the U.S. Navy | domínio público |
| 3 | O desenho que começou tudo (novo slide) | `cajal-purkinje.jpg` | [Cajal - a purkinje neuron from the human cerebellum](https://commons.wikimedia.org/wiki/File:Cajal_-_a_purkinje_neuron_from_the_human_cerebellum.jpg) | Santiago Ramón y Cajal (Cajal Institute, CSIC) | domínio público |
| 4 | Os rostos desta história (novo slide) | `pitts-1954.jpg` | [1954 Walter Pitts and a blackboard](https://commons.wikimedia.org/wiki/File:1954_Walter_Pitts_and_a_blackboard.jpg) | Francis Bello (MIT) | domínio público |
| 5 | idem | `rosenblatt.jpg` | [Frank Rosenblatt](https://commons.wikimedia.org/wiki/File:Frank_Rosenblatt.jpg) | desconhecido | CC BY-SA 4.0 |
| 6 | idem | `widrow-adaline.jpg` | [Bernard Widrow with ADALINE](https://commons.wikimedia.org/wiki/File:Bernard_Widrow_with_ADALINE.jpg) | Stanford Today (1963) | domínio público |
| 7 | idem | `minsky.jpg` | [Marvin Minsky at OLPCb (3x4 cropped)](https://commons.wikimedia.org/wiki/File:Marvin_Minsky_at_OLPCb_(3x4_cropped).jpg) | Seth Woodworth | CC BY 3.0 |
| 8 | idem | `papert.jpg` | [Seymour Papert](https://commons.wikimedia.org/wiki/File:Seymour_Papert.jpg) | Matematicamente.it | CC BY-SA 3.0 |
| 9 | idem | `rumelhart.jpg` | [David Rumelhart (IJCNN 1991)](https://commons.wikimedia.org/wiki/File:DavidRumelhart-IJCNNseattle1991-07-08.jpg) | Laniakea-rubikon | CC BY-SA 4.0 |
| 10 | O que uma rede profunda fez pela biologia | `alphafold-tmem253.jpg` | [TMEM253 AlphaFold Predicted Structure](https://commons.wikimedia.org/wiki/File:TMEM253_AlphaFold_Predicted_Structure.jpg) | AlphaFold DB (EMBL-EBI) | CC0 |
| 11 | A hierarquia que emerge sozinha | `alexnet-arch.png` | [AlexNet architecture](https://commons.wikimedia.org/wiki/File:AlexNet_architecture.png) | Daniel Voigt Godoy | CC BY 4.0 |
| 12 | (reserva — não usada nos slides) | `gpu-tesla.jpg` | [NvidiaTesla](https://commons.wikimedia.org/wiki/File:NvidiaTesla.jpg) | en:User:Mahogny | domínio público |

Observações:

- A foto antiga do Hinton (Eviatar Bach, "Geoffrey Hinton at Cambridge")
  não existe mais no Commons com esse nome; foi substituída pela foto da
  coletiva do Nobel 2024 (Hopfield + Hinton), mais atual e temática.
- `gpu-tesla.jpg` ficou de reserva: a caixa "Hardware" do slide "Por que
  só agora?" não comportou a foto sem estourar o frame (padrão zero
  Overfull). Ela pode ser aproveitada em aulas sobre treinamento/GPUs.
- Candidatas avaliadas e descartadas: retrato do Hebb (só existe fair-use
  na en-wiki), retrato do McCulloch (sem foto livre no Commons), figura
  original do AlexNet do paper (copyright NeurIPS), figura do Transformer
  (CC BY-SA 3.0 — boa para a aula de atenção/Transformers no fim do
  curso), foto do trio Nobel de Química 2024 (Baker/Hassabis/Jumper, CC
  BY-SA 4.0 — boa para a aula de AlphaFold se quiser mais gente).

### Como baixar / atualizar

```bash
bash aula01/imagens/baixar-imagens.sh
```

O script registra, arquivo por arquivo, a URL original, o autor e a
licença. Os arquivos já estão baixados no repositório — o script serve
para restaurar/atualizar.

---

## 2. Links e vídeos complementares por assunto

Os 13 links abaixo estão no slide "Para saber mais — sites e vídeos por
assunto" (todos verificados em 2026-08-31).

### Fundamentos e história (coluna A do slide)

| Assunto | Link | Tipo |
|---------|------|------|
| O que é uma rede neural | [3Blue1Brown — "But what is a neural network?"](https://youtu.be/aircAruvnKk) | vídeo (18 min) |
| Série completa de redes neurais | [3Blue1Brown — playlist](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) | playlist (4 vídeos) |
| Introdução ao deep learning | [MIT 6.S191 — introtodeeplearning.com](https://introtodeeplearning.com) | curso + vídeos |
| O Mark I "aprende" a ler (1958) | [Newsreel "New Navy device learns by doing"](https://youtu.be/cNxadbrN_aI) | vídeo histórico |
| Aproximação universal, visual | [Nielsen — cap. 1 e 4](https://neuralnetworksanddeeplearning.com) | texto interativo |
| Perceptron em português | [Wikipedia — Perceptron (pt)](https://pt.wikipedia.org/wiki/Perceptron) | verbete |
| Profundidade vs. largura | [CMU 11-785 — deeplearning.cs.cmu.edu](https://deeplearning.cs.cmu.edu) | palestras 1–2 |

### Deep learning hoje (coluna B do slide)

| Assunto | Link | Tipo |
|---------|------|------|
| Nobel de Física 2024 | [Comunicado oficial](https://www.nobelprize.org/prizes/physics/2024/press-release/) | texto oficial |
| AlphaFold | [DeepMind — blog oficial](https://deepmind.google/discover/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/) | blog + vídeo |
| PyTorch do zero | [Tutorial oficial "Learn the Basics"](https://pytorch.org/tutorials/beginner/basics/intro.html) | tutorial |
| Retropropagação do zero | [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) | curso em vídeo |
| Atenção e Transformers | [3Blue1Brown — "Attention in transformers"](https://youtu.be/eMlx5fFNoYc) | vídeo (26 min) |
| O que cada camada aprende | [distill.pub — Feature Visualization](https://distill.pub/2017/feature-visualization/) | artigo interativo |

### Extras que ficaram de fora do slide (na referência ou para outras aulas)

| Assunto | Link | Observação |
|---------|------|------------|
| Visualizando CNNs | [Zeiler & Fergus (2014), arXiv:1311.2901](https://arxiv.org/abs/1311.2901) | já citado na referência da aula |
| Profundidade vs. largura (formal) | [Telgarsky (2016), arXiv:1602.04420](https://arxiv.org/abs/1602.04420) | já citado na referência |
| Aprendizado por reforço | [OpenAI Spinning Up](https://spinningup.openai.com/) | bom para o paradigma por reforço (seção 5) |
| AlphaFold em vídeo | [DeepMind — vídeo de anúncio](https://youtu.be/gg7WjuFs8F4) | 3 min, ótimo para abrir a aula |
| Arquitetura do Transformer | [Figura CC BY-SA 3.0 no Commons](https://commons.wikimedia.org/wiki/File:The-Transformer-model-architecture.png) | usar na aula de atenção |
| História das redes neurais | [Wikipedia (en) — History of artificial neural networks](https://en.wikipedia.org/wiki/History_of_artificial_neural_networks) | leitura complementar |

Nota: `neuralnetworksanddeeplearning.com` (Nielsen) estava com instabilidade
de rede no dia da verificação, mas é a referência canônica — mantida.

---

## 3. Mudanças feitas na aula (aula01.tex)

1. **Preamble**: `\usepackage{listings}` + `\lstset{basicstyle=\ttfamily\footnotesize}` —
   os dois frames de código agora cabem sem estourar.
2. **"O momento em que estamos"**: foto do Nobel 2024 (Hopfield + Hinton) no lugar da
   foto antiga do Hinton (crédito atualizado).
3. **"O que uma rede profunda fez pela biologia"**: diagrama + imagem da estrutura
   prevista pelo AlphaFold lado a lado (colunas).
4. **Novo frame "Os rostos desta história"** (após a linha do tempo): galeria
   Pitts / Rosenblatt / Widrow / Minsky / Papert / Rumelhart, com créditos.
5. **Novo frame "O desenho que começou tudo"** (antes de "O original biológico"):
   desenho de Cajal + a ponte para McCulloch–Pitts.
6. **"Perceptrons são portas lógicas"** e **"Uma camada oculta resolve o XOR"**:
   tikzpictures agora em `\scalebox` (cabiam 1–2 mm fora da coluna).
7. **"A hierarquia que emerge sozinha"**: figura do AlexNet (redesenhada, CC BY 4.0)
   no lugar do diagrama de blocos.
8. **Novo frame "Para saber mais — sites e vídeos por assunto"** (antes de "Para
   casa"): os 13 links da seção 2.
9. **Referências**: créditos de todas as imagens.

Padrão mantido: **zero Overfull** (verificado com `xelatex | grep Overfull`,
duas passadas) e compilação com `latexmk -xelatex`.

---

## 4. Critérios usados na seleção

- Preferência por **domínio público** (retratos históricos, fotos da
  Marinha, desenhos de Cajal); CC BY/CC BY-SA/CC0 quando não havia PD.
- Sem imagens "fair use" (ex.: Hebb, AlexNet original do paper).
- Tamanho e orientação compatíveis com o `\fotoslot` (que já tem fallback
  para placeholder se a imagem faltar).
- Links verificados por HTTP (200) no dia; vídeos são do YouTube oficial
  dos canais (3Blue1Brown, MIT, DeepMind) ou arquivos históricos.
