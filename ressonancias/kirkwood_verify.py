"""Verificação das lacunas de Kirkwood: teoria (Kepler), simulação e dados reais do JPL.

Lê ressonancias/dados/*.npz e *.json; imprime e grava os números em
ressonancias/dados/verificacao.json (o RELATORIO.md cita esse arquivo).
"""

import json
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"
A_J = 5.2044

# nome -> razão período(asteroide)/período(Júpiter)
RESSONANCIAS = {
    "3:1": 1 / 3,
    "5:2": 2 / 5,
    "7:3": 3 / 7,
    "2:1": 1 / 2,
    "3:2": 2 / 3,
}
JAN_RES = 0.02
JAN_VIZ = (0.05, 0.15)
BIN = 0.01
FAIXA = (2.0, 4.4)


def a_teorica(razao):
    return A_J * razao ** (2 / 3)


def contagem(a, centro, w):
    return int(np.sum(np.abs(a - centro) <= w))


def efeito(a, centro):
    """Contagem em ±0,02 UA contra a densidade de vizinhança (0,05 a 0,15 UA, dois lados)."""
    obs = contagem(a, centro, JAN_RES)
    d = np.abs(a - centro)
    viz = int(np.sum((d > JAN_VIZ[0]) & (d <= JAN_VIZ[1])))
    larg_viz = 2 * (JAN_VIZ[1] - JAN_VIZ[0])
    esp = viz / larg_viz * (2 * JAN_RES)
    pct = (obs / esp - 1) * 100 if esp > 0 else float("nan")
    sig = (obs - esp) / np.sqrt(esp) if esp > 0 else float("nan")
    return {"obs": obs, "esperado": round(esp, 2), "variacao_pct": round(pct, 1),
            "sigma_poisson": round(sig, 1)}


def tabela(a):
    return {nome: efeito(a, a_teorica(r)) for nome, r in RESSONANCIAS.items()}


def carrega_sbdb():
    linhas = []
    for nome in ("sbdb_mba.json", "sbdb_externo.json"):
        d = json.load(open(DADOS / nome))
        linhas += [(float(x[0]), float(x[1])) for x in d["data"] if x[0] is not None]
    a = np.array([l[0] for l in linhas])
    return a[(a >= FAIXA[0]) & (a <= FAIXA[1])]


def main():
    snaps = np.load(DADOS / "kirkwood_snapshots.npz")
    saida = {"posicoes_teoricas_UA": {n: round(a_teorica(r), 3) for n, r in RESSONANCIAS.items()}}
    saida["simulacao"] = {}
    for k, t in enumerate(snaps["t"]):
        a = snaps["a"][k][snaps["vivo"][k]]
        a = a[(a >= FAIXA[0]) & (a <= FAIXA[1])]
        saida["simulacao"][f"{t:.0f}"] = {"vivas": int(snaps["vivo"][k].sum()),
                                           "na_faixa": int(a.size), "ressonancias": tabela(a)}
    saida["tentativas"] = {}
    for nome in ("A", "B", "C"):
        f = DADOS / f"kirkwood_tent_{nome}.npz"
        if not f.exists():
            continue
        d = np.load(f)
        amin, amax = float(d["a0"].min()), float(d["a0"].max())
        res = {}
        for k, t in enumerate(d["t"]):
            a = d["a"][k][d["vivo"][k]]
            tab = {}
            for n_, r in RESSONANCIAS.items():
                c = a_teorica(r)
                if c - JAN_VIZ[1] >= amin and c + JAN_VIZ[1] <= amax:
                    tab[n_] = efeito(a, c)
            res[f"{t:.0f}"] = {"vivas": int(d["vivo"][k].sum()), "ressonancias": tab}
        saida["tentativas"][nome] = {"n": int(d["n"]), "a0": [round(amin, 3), round(amax, 3)],
                                      "e0_max": round(float(d["e0"].max()), 3), "ressonancias_por_t": res,
                                      "tempo_execucao_s": round(float(d["tempo_execucao_s"]))}
    f2 = DADOS / "kirkwood_v2_snapshots.npz"
    if f2.exists():
        d = np.load(f2)
        v2 = {"n": int(d["n"]), "e0_media": round(float(d["e0"].mean()), 3),
              "e0_sem_dado": int(d["e0_sem_dado"]), "tempo_execucao_s": round(float(d["tempo_execucao_s"])),
              "criterios": {}, "borda_interna": {}}
        for crit, chave in (("marte_q<1,67", "vivo_marte"), ("antigo_r<1_e>0,7", "vivo_old")):
            por_t = {}
            for k, t in enumerate(d["t"]):
                viv = d[chave][k]
                a = d["a"][k][viv]
                a = a[(a >= FAIXA[0]) & (a <= FAIXA[1])]
                por_t[f"{t:.0f}"] = {"vivas": int(viv.sum()), "ressonancias": tabela(a)}
            v2["criterios"][crit] = por_t
        a0 = d["a0"]
        for lo, hi in ((2.0, 2.2), (2.2, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.2)):
            m = (a0 >= lo) & (a0 < hi)
            linha = {}
            for k, t in enumerate(d["t"]):
                viv = d["vivo_marte"][k] & m
                linha[f"{t:.0f}"] = {"inicio": int(m.sum()), "vivas_marte": int(viv.sum()),
                                      "e_medio_vivas": round(float(d["e"][k][viv].mean()), 3) if viv.any() else None}
            v2["borda_interna"][f"{lo}-{hi}"] = linha
        saida["v2"] = v2
        print("v2:", json.dumps(v2["criterios"]["marte_q<1,67"][f"{d['t'][-1]:.0f}"]["ressonancias"]))
    real = carrega_sbdb()
    saida["jpl_sbdb"] = {"n": int(real.size), "ressonancias": tabela(real)}
    json.dump(saida, open(DADOS / "verificacao.json", "w"), indent=1, ensure_ascii=False)
    for n, v in saida["posicoes_teoricas_UA"].items():
        print("teoria", n, v)
    for t, v in saida["simulacao"].items():
        print("sim t=", t, "vivas", v["vivas"])
        for n, r in v["ressonancias"].items():
            print("   ", n, r)
    for nome, v in saida["tentativas"].items():
        print("tentativa", nome, v["n"], v["a0"], "e0max", v["e0_max"])
        for t, r in v["ressonancias_por_t"].items():
            print("   t=", t, "vivas", r["vivas"], r["ressonancias"])
    print("JPL n=", saida["jpl_sbdb"]["n"])
    for n, r in saida["jpl_sbdb"]["ressonancias"].items():
        print("   ", n, r)


if __name__ == "__main__":
    main()
