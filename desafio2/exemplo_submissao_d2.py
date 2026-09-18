"""
exemplo_submissao_d2.py — exemplo de entrega do Desafio 2
Entrega oficial: copie para desafio2/desafio2_nomes.py no seu repositório.
Ideia: em vez de decorar Xavier/He, CALIBRAR o ganho numericamente para a ativação escolhida.
Se z ~ N(0, 1) e W ~ N(0, s^2), a pré-ativação da próxima camada tem variância
    fan_in * s^2 * E[f(z)^2]
Para mantê-la em 1 camada após camada:  s^2 = 1 / (fan_in * E[f(z)^2]).
Troque `ativacao` por outra função e a inicialização se ajusta sozinha.
Rode:  python harness_desafio2.py exemplo_submissao_d2.py --rapido

Referências da API do PyTorch usadas aqui:
  torch.nn.functional.gelu   https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gelu.html
  torch.Tensor.normal_       https://docs.pytorch.org/docs/stable/generated/torch.Tensor.normal_.html
  torch.Tensor.zero_         https://docs.pytorch.org/docs/stable/generated/torch.Tensor.zero_.html
  torch.no_grad              https://docs.pytorch.org/docs/stable/generated/torch.no_grad.html
  torch.Generator            https://docs.pytorch.org/docs/stable/generated/torch.Generator.html
  torch.nn.init (Xavier, He, calculate_gain — para comparar com a conta feita à mão)
                             https://docs.pytorch.org/docs/stable/nn.init.html
  outras ativações: relu, leaky_relu, elu, selu, silu em https://docs.pytorch.org/docs/stable/nn.functional.html#non-linear-activation-functions
"""
import math
import torch


def ativacao(x: torch.Tensor) -> torch.Tensor:
    return torch.nn.functional.gelu(x)          # elemento a elemento, sem parâmetros


# E[f(z)^2] com z ~ N(0,1), estimado uma vez por amostragem (Monte Carlo)
_g = torch.Generator().manual_seed(0)
_E_f2 = ativacao(torch.randn(1_000_000, generator=_g)).pow(2).mean().item()


@torch.no_grad()
def inicializar(W: torch.Tensor, b: torch.Tensor,
                fan_in: int, fan_out: int, camada: int, n_camadas: int) -> None:
    desvio = math.sqrt(1.0 / (fan_in * _E_f2))
    if camada == n_camadas:                      # camada de logits: um pouco menor ajuda o SGD
        desvio *= 0.5
    W.normal_(0.0, desvio)
    b.zero_()
