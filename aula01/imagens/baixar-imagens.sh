#!/usr/bin/env bash
# ============================================================
# baixar-imagens.sh — Aula 1 (GBC073): imagens dos slides
# ------------------------------------------------------------
# Uso:  bash baixar-imagens.sh
# Rode dentro de aula01/ (ou de onde estiver; o script se
# localiza sozinho). Baixa do Wikimedia Commons todas as fotos
# usadas nos slides. Cada bloco documenta:
#   arquivo de destino | arquivo Commons | autor | licença
#
# Política do Wikimedia: pede User-Agent identificando o
# projeto — o curl abaixo sempre envia um.
# ============================================================
set -euo pipefail

UA="GBC073-aula01/1.0 (material didatico FACOM/UFU; contato: professor)"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. Nobel 2024 — Hopfield e Hinton na coletiva do prêmio
#    File:John J. Hopfield and Geoffrey E. Hinton, 2024 Nobel Prize Laureate in Physics.jpg
#    Autor: Arthur Petron  |  CC BY-SA 4.0
curl -sSL -A "$UA" -o nobel-2024.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/8/8f/John_J._Hopfield_and_Geoffrey_E._Hinton%2C_2024_Nobel_Prize_Laureate_in_Physics.jpg"

# 2. Mark I Perceptron (Cornell, 1960) — foto oficial da Marinha dos EUA
#    File:330-PSA-80-60 (USN 710739) (20897323365).jpg
#    National Museum of the U.S. Navy  |  domínio público
curl -sSL -A "$UA" -o mark1.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/1/1a/330-PSA-80-60_%28USN_710739%29_%2820897323365%29.jpg"

# 3. Neurônio de Purkinje desenhado por Cajal (1899)
#    File:Cajal - a purkinje neuron from the human cerebellum.jpg
#    Santiago Ramón y Cajal  |  domínio público (Cajal Institute, CSIC)
curl -sSL -A "$UA" -o cajal-purkinje.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/7/77/Cajal_-_a_purkinje_neuron_from_the_human_cerebellum.jpg"

# 4. Walter Pitts no quadro-negro do MIT (1954)
#    File:1954 Walter Pitts and a blackboard.jpg
#    Foto: Francis Bello  |  domínio público
curl -sSL -A "$UA" -o pitts-1954.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/a/a0/1954_Walter_Pitts_and_a_blackboard.jpg"

# 5. Frank Rosenblatt (jovem)
#    File:Frank Rosenblatt.jpg  |  autor desconhecido  |  CC BY-SA 4.0
curl -sSL -A "$UA" -o rosenblatt.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/3/3b/Frank_Rosenblatt.jpg"

# 6. Bernard Widrow com o ADALINE (Stanford Today, 1963)
#    File:Bernard Widrow with ADALINE.jpg  |  domínio público
curl -sSL -A "$UA" -o widrow-adaline.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/c/ce/Bernard_Widrow_with_ADALINE.jpg"

# 7. Marvin Minsky (OLPC)
#    File:Marvin Minsky at OLPCb (3x4 cropped).jpg
#    Foto: Seth Woodworth  |  CC BY 3.0
curl -sSL -A "$UA" -o minsky.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/f/f9/Marvin_Minsky_at_OLPCb_%283x4_cropped%29.jpg"

# 8. Seymour Papert
#    File:Seymour Papert.jpg  |  Matematicamente.it  |  CC BY-SA 3.0
curl -sSL -A "$UA" -o papert.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/7/74/Seymour_Papert.jpg"

# 9. David Rumelhart (IJCNN Seattle, 1991)
#    File:DavidRumelhart-IJCNNseattle1991-07-08.jpg  |  CC BY-SA 4.0
curl -sSL -A "$UA" -o rumelhart.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/7/72/DavidRumelhart-IJCNNseattle1991-07-08.jpg"

# 10. Estrutura de proteína prevista pelo AlphaFold (TMEM253, colorida por pLDDT)
#     File:TMEM253 AlphaFold Predicted Structure.jpg  |  CC0
curl -sSL -A "$UA" -o alphafold-tmem253.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/5/5d/TMEM253_AlphaFold_Predicted_Structure.jpg"

# 11. Arquitetura do AlexNet (Krizhevsky et al., 2012) — redrawn
#     File:AlexNet architecture.png  |  Daniel Voigt Godoy  |  CC BY 4.0
curl -sSL -A "$UA" -o alexnet-arch.png \
  "https://upload.wikimedia.org/wikipedia/commons/1/1d/AlexNet_architecture.png"

# 12. Placa GPU Nvidia Tesla
#     File:NvidiaTesla.jpg  |  domínio público
#     (usa o thumb 1280px: o original em upload.wikimedia.org tem
#     respondido com erro 5xx; o thumb é suficiente para o slide)
curl -sSL -A "$UA" -o gpu-tesla.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/NvidiaTesla.jpg/1280px-NvidiaTesla.jpg"

echo "OK: $(ls -1 | wc -l) arquivos em $(pwd)"
