"""
harness_desafio2.py — Desafio 2: Ativação e inicialização em redes profundas (sem normalização)
GBC073 — Inteligência Computacional (FACOM/UFU) — Prof. Marcelo Keese Albertini

O ALUNO ENTREGA, no próprio repositório, o arquivo desafio2/desafio2_nomes.py com duas funções:

    def ativacao(x: torch.Tensor) -> torch.Tensor
        # elemento a elemento, sem parâmetros, sem olhar o lote; a derivada vem do autograd

    @torch.no_grad()
    def inicializar(W: torch.Tensor, b: torch.Tensor,
                    fan_in: int, fan_out: int, camada: int, n_camadas: int) -> None
        # preenche W (fan_out, fan_in) e b (fan_out,) IN-PLACE; camada = 1..n_camadas

O HARNESS constrói um MLP de largura 256 e profundidade L ∈ {4, 16, 48}, SEM BatchNorm,
SEM conexões residuais, alternando Linear -> ativacao; inicializa cada camada com
inicializar(); treina 3 épocas com SGD (momento 0,9, lr 0,05, lote 128, entropia cruzada);
mede a acurácia de teste. Também imprime um "raio-X" da propagação de sinal no passo 0.

Escore: s_t = clip((m - baseline)/(referencia - baseline), 0, 1.25)
        S   = 100 * (0.7*média(s_t) + 0.3*mín(s_t))
Baseline:   tanh + U(-0.05, 0.05).       Referência: ReLU + He normal, viés zero.

Uso:
    python harness_desafio2.py                         # baseline e referência, tarefas públicas
    python harness_desafio2.py desafio2/desafio2_nomes.py   # avalia a submissão
    python harness_desafio2.py desafio2/desafio2_nomes.py --rapido    # 10% dos dados, 1 época: teste de fumaça
    python harness_desafio2.py desafio2/desafio2_nomes.py --ocultas   # professor: usa ocultas_d2.py, se existir
    python harness_desafio2.py --calibrar              # recalcula e grava calibracao_d2.json

Baseline e referência são caros (treinam 9+ redes); ficam em cache em calibracao_d2.json.
Dependências: torch, torchvision (baixa MNIST/FashionMNIST/CIFAR-10 em ./dados).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import time
from dataclasses import dataclass, field
from typing import Callable

import torch
import torch.nn as nn
import torch.nn.functional as F

# =============================================================================
# 0. Constantes do desafio (fixas)
# =============================================================================
LARGURA = 256
PROFUNDIDADES = (4, 16, 48)
EPOCAS = 3
LR = 0.05
MOMENTO = 0.9
LOTE = 128
SEMENTES = (0, 1, 2)
TETO_BONUS = 1.25
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DIR_DADOS = "./dados"
ARQ_CALIB = "calibracao_d2.json"

# =============================================================================
# 1. Dados: tensores achatados e padronizados em memória
# =============================================================================
_cache_dados: dict[str, tuple] = {}
GERADORES_EXTRA: dict[str, Callable] = {}         # ocultas_d2.py pode registrar geradores aqui


def _torchvision(nome: str):
    import torchvision
    cls = getattr(torchvision.datasets, {"mnist": "MNIST", "fashion": "FashionMNIST",
                                         "cifar10": "CIFAR10"}.get(nome, nome))
    tr = cls(DIR_DADOS, train=True, download=True)
    te = cls(DIR_DADOS, train=False, download=True)
    def tens(ds):
        X = torch.as_tensor(ds.data if hasattr(ds, "data") else ds.train_data)
        X = X.float().reshape(len(X), -1) / 255.0
        y = torch.as_tensor(ds.targets).long()
        return X, y
    Xtr, ytr = tens(tr); Xte, yte = tens(te)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    return (Xtr - mu) / sd, ytr, (Xte - mu) / sd, yte, 10


def dados(nome: str):
    if nome not in _cache_dados:
        if nome in GERADORES_EXTRA:                       # datasets definidos em ocultas_d2.py
            _cache_dados[nome] = GERADORES_EXTRA[nome]()
        else:
            _cache_dados[nome] = _torchvision(nome)
    return _cache_dados[nome]

# =============================================================================
# 2. Modelo: MLP nu — a submissão controla só a não linearidade e a escala inicial
# =============================================================================
class MLP(nn.Module):
    def __init__(self, d_in, n_classes, L, largura, sub):
        super().__init__()
        dims = [d_in] + [largura] * (L - 1) + [n_classes]
        self.camadas = nn.ModuleList(nn.Linear(dims[i], dims[i + 1]) for i in range(L))
        self.ativ = sub.ativacao
        with torch.no_grad():
            for k, lin in enumerate(self.camadas, start=1):
                sub.inicializar(lin.weight, lin.bias, lin.in_features, lin.out_features, k, L)
                assert torch.isfinite(lin.weight).all() and torch.isfinite(lin.bias).all(), \
                    f"inicializar produziu NaN/Inf na camada {k}"

    def forward(self, x, raio_x: list | None = None):
        for k, lin in enumerate(self.camadas):
            x = lin(x)
            if raio_x is not None:
                raio_x.append(x.detach().float().var().item())     # variância da pré-ativação
            if k < len(self.camadas) - 1:                           # última camada: logits
                x = self.ativ(x)
        return x

# =============================================================================
# 3. Verificações da caixa-preta
# =============================================================================
class Violacao(Exception):
    pass


def checar_ativacao(f: Callable):
    torch.manual_seed(0)
    x = torch.randn(64, 32, device=DEVICE)
    y = f(x)
    if not torch.is_tensor(y) or y.shape != x.shape:
        raise Violacao("ativacao deve devolver tensor com a MESMA forma da entrada")
    if not torch.isfinite(y).all():
        raise Violacao("ativacao devolveu NaN/Inf para entrada gaussiana")
    # elemento a elemento: perturbar (0,0) só pode mudar (0,0)
    x2 = x.clone(); x2[0, 0] += 0.37
    d = (f(x2) - y).abs()
    if d.sum() - d[0, 0] > 1e-6:
        raise Violacao("ativacao não é elemento a elemento (BatchNorm/LayerNorm disfarçados não valem)")
    # sem dependência do lote: permutar linhas permuta a saída
    perm = torch.randperm(64)
    if not torch.allclose(f(x[perm]), y[perm], atol=1e-6):
        raise Violacao("ativacao depende do lote")
    # determinística e sem estado
    if not torch.allclose(f(x), y, atol=1e-6):
        raise Violacao("ativacao não é determinística")
    # diferenciável pelo autograd
    xg = x.clone().requires_grad_(True)
    f(xg).sum().backward()
    if xg.grad is None or not torch.isfinite(xg.grad).all():
        raise Violacao("ativacao não tem gradiente definido (use operações do torch)")


def checar_inicializar(g: Callable):
    W = torch.empty(16, 8, device=DEVICE); b = torch.empty(16, device=DEVICE)
    with torch.no_grad():
        r = g(W, b, 8, 16, 1, 4)
    if not (torch.isfinite(W).all() and torch.isfinite(b).all()):
        raise Violacao("inicializar deixou NaN/Inf (esqueceu de preencher in-place?)")
    if r is not None and torch.is_tensor(r):
        raise Violacao("inicializar deve preencher W e b IN-PLACE e devolver None")

# =============================================================================
# 4. Uma execução (dataset, L, largura, semente) -> acurácia de teste  [+ raio-X]
# =============================================================================
@dataclass
class Resultado:
    acc: float
    var_pre_ativ: list = field(default_factory=list)   # por camada, passo 0
    norma_grad: list = field(default_factory=list)     # por camada, passo 0
    tempo_s: float = 0.0


def rodar(sub, nome_dados: str, L: int, largura: int, semente: int,
          fracao: float = 1.0, epocas: int = EPOCAS) -> Resultado:
    Xtr, ytr, Xte, yte, C = dados(nome_dados)
    if fracao < 1.0:
        n = int(len(Xtr) * fracao); Xtr, ytr = Xtr[:n], ytr[:n]
        m = int(len(Xte) * fracao); Xte, yte = Xte[:m], yte[:m]
    Xtr, ytr, Xte, yte = (t.to(DEVICE) for t in (Xtr, ytr, Xte, yte))

    torch.manual_seed(semente)
    modelo = MLP(Xtr.shape[1], C, L, largura, sub).to(DEVICE)
    opt = torch.optim.SGD(modelo.parameters(), lr=LR, momentum=MOMENTO)
    g = torch.Generator(device="cpu").manual_seed(semente)

    # raio-X no passo 0 (não pontua; explica o resultado)
    res = Resultado(acc=0.0)
    xb, yb = Xtr[:LOTE], ytr[:LOTE]
    logits = modelo(xb, raio_x=res.var_pre_ativ)
    F.cross_entropy(logits, yb).backward()
    res.norma_grad = [lin.weight.grad.norm().item() for lin in modelo.camadas]
    opt.zero_grad()

    t0 = time.perf_counter()
    modelo.train()
    for _ in range(epocas):
        for idx in torch.randperm(len(Xtr), generator=g).split(LOTE):
            idx = idx.to(DEVICE)
            perda = F.cross_entropy(modelo(Xtr[idx]), ytr[idx])
            if not torch.isfinite(perda):
                res.acc = 1.0 / C; res.tempo_s = time.perf_counter() - t0   # divergiu: chance
                return res
            opt.zero_grad(); perda.backward(); opt.step()
    res.tempo_s = time.perf_counter() - t0

    modelo.eval()
    with torch.no_grad():
        acertos = sum((modelo(Xte[i:i + 2048]).argmax(1) == yte[i:i + 2048]).sum().item()
                      for i in range(0, len(Xte), 2048))
    res.acc = acertos / len(Xte)
    return res

# =============================================================================
# 5. Baseline e referência do professor
# =============================================================================
class Baseline:
    """tanh + uniforme pequena: treina em L=4, morre em L=48 (gradiente some)."""
    @staticmethod
    def ativacao(x): return torch.tanh(x)
    @staticmethod
    @torch.no_grad()
    def inicializar(W, b, fan_in, fan_out, camada, n_camadas):
        W.uniform_(-0.05, 0.05); b.zero_()


class Referencia:
    """ReLU + He normal (He et al., 2015), viés zero."""
    @staticmethod
    def ativacao(x): return torch.relu(x)
    @staticmethod
    @torch.no_grad()
    def inicializar(W, b, fan_in, fan_out, camada, n_camadas):
        W.normal_(0.0, math.sqrt(2.0 / fan_in)); b.zero_()

# =============================================================================
# 6. Tarefas e escore
# =============================================================================
@dataclass
class Tarefa:
    nome: str
    dados: str
    L: int
    largura: int = LARGURA
    oculta: bool = False


def tarefas_publicas() -> list[Tarefa]:
    return [Tarefa(f"{d}_L{L}", d, L) for d in ("mnist", "fashion", "cifar10") for L in PROFUNDIDADES]


def tarefas_ocultas() -> list[Tarefa]:
    """As tarefas ocultas ficam em um arquivo privado do professor (ocultas_d2.py), que define
    OCULTAS: list[Tarefa]. Se o arquivo não existir, --ocultas não acrescenta nada."""
    try:
        from ocultas_d2 import OCULTAS
        return [Tarefa(t.nome, t.dados, t.L, t.largura, oculta=True) for t in OCULTAS]
    except ImportError:
        print("  (ocultas_d2.py não encontrado: avaliando só as tarefas públicas)")
        return []


def escore_tarefa(m, b, r, teto=TETO_BONUS):
    return float(min(max((m - b) / max(r - b, 1e-3), 0.0), teto))


def _mediana(sub, t: Tarefa, sementes, fracao, epocas) -> tuple[float, Resultado]:
    rs = [rodar(sub, t.dados, t.L, t.largura, s, fracao, epocas) for s in sementes]
    accs = torch.tensor([r.acc for r in rs])
    return accs.median().item(), rs[0]


def calibrar(tarefas: list[Tarefa], sementes, fracao, epocas, arq=ARQ_CALIB, forcar=False) -> dict:
    """Baseline e referência por tarefa, em cache. Chave inclui fracao/epocas (modo rápido)."""
    cache = json.load(open(arq)) if (os.path.exists(arq) and not forcar) else {}
    mudou = False
    for t in tarefas:
        chave = f"{t.nome}|f={fracao}|e={epocas}|dev={DEVICE.type}"
        if chave not in cache:
            print(f"  calibrando {t.nome} ...", end="", flush=True)
            b, _ = _mediana(Baseline, t, sementes, fracao, epocas)
            r, _ = _mediana(Referencia, t, sementes, fracao, epocas)
            cache[chave] = {"baseline": b, "referencia": r}; mudou = True
            print(f" baseline={b:.3f} referência={r:.3f}")
    if mudou:
        json.dump(cache, open(arq, "w"), indent=1)
    return {t.nome: cache[f"{t.nome}|f={fracao}|e={epocas}|dev={DEVICE.type}"] for t in tarefas}


def _raio_x(res: Resultado) -> str:
    """Resumo compacto: variância da pré-ativação e norma do gradiente na 1ª, meio e última camada."""
    v, gr = res.var_pre_ativ, res.norma_grad
    if not v:
        return ""
    ids = sorted({0, len(v) // 2, len(v) - 1})
    var_s = " ".join(f"{v[i]:.2g}" for i in ids)
    grad_s = " ".join(f"{gr[i]:.2g}" for i in ids)
    return f"var(pré-ativ) 1ª/meio/última: {var_s} | ‖grad W‖: {grad_s}"


def avaliar(sub, tarefas: list[Tarefa], calib: dict, sementes=SEMENTES,
            fracao=1.0, epocas=EPOCAS, verboso=True):
    try:
        checar_ativacao(sub.ativacao); checar_inicializar(sub.inicializar)
    except Violacao as e:
        print(f"  SUBMISSÃO INVÁLIDA: {e}"); return 0.0, []
    linhas, s = [], []
    for t in tarefas:
        b, r = calib[t.nome]["baseline"], calib[t.nome]["referencia"]
        erro, rx = None, ""
        try:
            m, res0 = _mediana(sub, t, sementes, fracao, epocas); rx = _raio_x(res0)
        except Violacao as e:
            m, erro = b, str(e)
        except Exception as e:
            m, erro = b, f"{type(e).__name__}: {e}"
        st = escore_tarefa(m, b, r); s.append(st)
        linhas.append(dict(tarefa=t.nome, oculta=t.oculta, acc=round(m, 4), baseline=round(b, 4),
                           referencia=round(r, 4), s_t=round(st, 3), raio_x=rx, erro=erro))
        if verboso:
            tag = "[oculta] " if t.oculta else ""
            print(f"  {tag}{t.nome:<18} acc={m:5.3f}  base={b:5.3f}  ref={r:5.3f}  s_t={st:4.2f}"
                  + (f"   ANULADA: {erro}" if erro else ""))
            if rx and not erro:
                print(f"  {'':18} {rx}")
    st_t = torch.tensor(s)
    S = 100.0 * (0.7 * st_t.mean().item() + 0.3 * st_t.min().item())
    if verboso:
        print(f"  {'-'*76}\n  ESCORE S = {S:6.1f}   (média={st_t.mean():.2f}, mínimo={st_t.min():.2f})")
    return S, linhas

# =============================================================================
# 7. Linha de comando
# =============================================================================
def carregar_submissao(caminho: str):
    spec = importlib.util.spec_from_file_location("submissao_aluno", caminho)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for f in ("ativacao", "inicializar"):
        if not callable(getattr(mod, f, None)):
            raise SystemExit(f"o arquivo precisa definir a função {f}()")
    return mod


def main():
    ap = argparse.ArgumentParser(description="Harness do Desafio 2 (GBC073)")
    ap.add_argument("submissao", nargs="?", help="arquivo .py com ativacao() e inicializar()")
    ap.add_argument("--ocultas", action="store_true", help="inclui as tarefas ocultas")
    ap.add_argument("--rapido", action="store_true", help="10%% dos dados, 1 época, 1 semente")
    ap.add_argument("--sementes", type=int, default=len(SEMENTES), help="número de sementes (1-3)")
    ap.add_argument("--calibrar", action="store_true", help="recalcula baseline/referência e grava o cache")
    ap.add_argument("--json", help="grava o detalhamento em JSON")
    args = ap.parse_args()

    fracao, epocas = (0.1, 1) if args.rapido else (1.0, EPOCAS)
    sementes = SEMENTES[:1] if args.rapido else SEMENTES[:max(1, min(3, args.sementes))]
    tarefas = tarefas_publicas() + (tarefas_ocultas() if args.ocultas else [])

    print(f"Desafio 2 — Ativação e inicialização em redes profundas  (torch {torch.__version__}, {DEVICE})")
    print(f"MLP largura {LARGURA}, L ∈ {PROFUNDIDADES}, SGD lr={LR} momento={MOMENTO}, "
          f"{epocas} época(s), {len(sementes)} semente(s){', modo rápido' if args.rapido else ''}\n")

    calib = calibrar(tarefas, sementes, fracao, epocas, forcar=args.calibrar)
    if args.submissao:
        sub = carregar_submissao(args.submissao)
        print(f"\nSubmissão: {args.submissao}")
        S, linhas = avaliar(sub, tarefas, calib, sementes, fracao, epocas)
        if args.json:
            with open(args.json, "w") as fh:
                json.dump(dict(escore=S, tarefas=linhas), fh, indent=2, ensure_ascii=False)
    elif not args.calibrar:
        print("\nBaseline (tanh + U(-0,05, 0,05)) — deve dar S = 0:")
        avaliar(Baseline, tarefas, calib, sementes, fracao, epocas)
        print("\nReferência (ReLU + He) — deve dar S = 100:")
        avaliar(Referencia, tarefas, calib, sementes, fracao, epocas)


if __name__ == "__main__":
    main()
