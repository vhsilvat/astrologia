"""Lacunas de Kirkwood, modelo v2: Sol (+ planetas internos) + Júpiter + Saturno, planar.

Mudanças em relação à v1 (ver canal/prompt_kirkwood.md, adendos 1 e 2):
 - Saturno como corpo massivo; massa de Mercúrio a Marte somada à do Sol.
 - excentricidade inicial amostrada do dado real do JPL (por faixa de a); a uniforme.
 - duas remoções registradas à parte: critério de Marte (periélio q < 1,67 UA ou r > 10 UA)
   e critério antigo (r < 1 UA, r > 10 UA ou e > 0,7). Uma só integração serve às duas.
 - 3 processos (multiprocessing), nice 10, uma thread por biblioteca.

Saída: ressonancias/dados/kirkwood_v2_snapshots.npz (e kirkwood_v2_w{i}.npz parciais).
Uso: python kirkwood_sim_v2.py [--anos 5e5] [--n 3000] [--saida kirkwood_v2]
"""

import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import argparse
import json
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"

SEMENTE = 20261021
G = 4.0 * np.pi**2
M_JUP, M_SAT = 9.5479e-4, 2.858e-4
M_INTERNOS = 5.97e-6  # Mercúrio + Vênus + Terra + Marte (≈1,66e-7 + 2,45e-6 + 3,00e-6 + 3,23e-7)
M_SOL = 1.0 + M_INTERNOS
# Elementos planares (a, e, longitude do periélio ϖ, longitude média L), época J2000 aproximada
JUP = dict(a=5.2044, e=0.0489, varpi=14.73, L=34.40)
SAT = dict(a=9.58, e=0.057, varpi=92.60, L=49.94)
N_MAS = 3  # Sol, Júpiter, Saturno
DT = 0.1
BLOCO = 5.0
Q_MARTE = 1.67
SNAPS = [0.0, 1e3, 1e4, 5e4, 1e5, 2e5, 5e5]
N_WORKERS = 3


def monta(a, e, om, M):
    import rebound

    sim = rebound.Simulation()
    sim.units = ("yr", "AU", "Msun")
    sim.add(m=M_SOL)
    for m, p in ((M_JUP, JUP), (M_SAT, SAT)):
        sim.add(m=m, a=p["a"], e=p["e"], omega=np.radians(p["varpi"]),
                M=np.radians(p["L"] - p["varpi"]), primary=sim.particles[0])
    sim.N_active = sim.N
    sim.integrator = "whfast"
    for ai, ei, oi, Mi in zip(a, e, om, M):
        sim.add(m=0.0, a=ai, e=ei, omega=oi, M=Mi, primary=sim.particles[0])
    sim.move_to_com()
    return sim


def elementos(xyz, vel):
    r = xyz[N_MAS:, :2] - xyz[0, :2]
    v = vel[N_MAS:, :2] - vel[0, :2]
    rn = np.hypot(r[:, 0], r[:, 1])
    inv_a = 2.0 / rn - (v**2).sum(axis=1) / (G * M_SOL)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(inv_a != 0, 1.0 / inv_a, np.inf)
    h = r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]
    ex = (v[:, 1] * h) / (G * M_SOL) - r[:, 0] / rn
    ey = (-v[:, 0] * h) / (G * M_SOL) - r[:, 1] / rn
    e = np.hypot(ex, ey)
    q = h**2 / (G * M_SOL) / (1.0 + e)
    return a, e, q, rn


def trabalha(args):
    idx, a0, e0, om0, M0, snaps_t, tf, prefixo = args
    os.nice(10)
    sim = monta(a0, e0, om0, M0)
    sim.dt = DT
    n = len(a0)
    vivo_old = np.ones(n, dtype=bool)
    vivo_mar = np.ones(n, dtype=bool)
    a_at, e_at = a0.copy(), e0.copy()
    ids = np.arange(n)
    S_t, S_a, S_e, S_o, S_m = [], [], [], [], []
    prox, t, t_ini = 0, 0.0, time.time()

    def grava():
        np.savez_compressed(DADOS / f"{prefixo}_w{idx}.npz", t=np.array(S_t), a=np.array(S_a),
                            e=np.array(S_e), vivo_old=np.array(S_o), vivo_marte=np.array(S_m),
                            a0=a0, e0=e0, parcial=(t < tf))

    while True:
        while prox < len(snaps_t) and snaps_t[prox] <= t + 1e-9 and snaps_t[prox] <= tf:
            S_t.append(snaps_t[prox]); S_a.append(a_at.copy()); S_e.append(e_at.copy())
            S_o.append(vivo_old.copy()); S_m.append(vivo_mar.copy())
            print(f"[w{idx}] t={snaps_t[prox]:.0f} anos, vivas(antigo)={vivo_old.sum()}, "
                  f"vivas(Marte)={vivo_mar.sum()}, {time.time()-t_ini:.0f}s", flush=True)
            prox += 1
            grava()
        if t >= tf - 1e-9:
            break
        t = min(t + BLOCO, tf)
        sim.integrate(t)
        xyz = np.zeros((sim.N, 3)); vel = np.zeros((sim.N, 3))
        sim.serialize_particle_data(xyz=xyz, vxvyvz=vel)
        a, e, q, rn = elementos(xyz, vel)
        a_at[ids], e_at[ids] = a, e
        mar = (q < Q_MARTE) | (rn > 10.0) | (rn < 1.0) | ~np.isfinite(a)
        old = (rn < 1.0) | (rn > 10.0) | (e > 0.7) | ~np.isfinite(a)
        vivo_mar[ids[mar]] = False
        vivo_old[ids[old]] = False
        if old.any():
            for i in np.sort(np.where(old)[0])[::-1]:
                sim.remove(int(i) + N_MAS)
            ids = ids[~old]
    grava()
    return time.time() - t_ini


def condicoes_iniciais(n, rng):
    """a uniforme; e amostrada de asteroides reais (JPL) com |a_real - a| <= 0,05."""
    a0 = rng.uniform(2.0, 4.2, n)
    om0 = rng.uniform(0, 2 * np.pi, n)
    M0 = rng.uniform(0, 2 * np.pi, n)
    ar, er = [], []
    for nome in ("sbdb_mba.json", "sbdb_externo.json"):
        for l in json.load(open(DADOS / nome))["data"]:
            if l[0] is not None and l[1] is not None:
                ar.append(float(l[0])); er.append(float(l[1]))
    ar, er = np.array(ar), np.array(er)
    ordem = np.argsort(ar)
    ar, er = ar[ordem], er[ordem]
    e0 = np.zeros(n)
    sem_dado = 0
    for i, a in enumerate(a0):
        lo, hi = np.searchsorted(ar, [a - 0.05, a + 0.05])
        if hi - lo >= 5:
            e0[i] = er[rng.integers(lo, hi)]
        else:
            e0[i] = rng.uniform(0.0, 0.2)
            sem_dado += 1
    return a0, e0, om0, M0, sem_dado


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anos", type=float, default=5e5)
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--saida", default="kirkwood_v2")
    args = ap.parse_args()
    DADOS.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEMENTE)
    a0, e0, om0, M0, sem_dado = condicoes_iniciais(args.n, rng)
    print(f"e inicial: média {e0.mean():.3f}, máx {e0.max():.3f}; {sem_dado} partículas sem dado "
          f"suficiente (e uniforme em [0; 0,2])", flush=True)
    blocos = np.array_split(np.arange(args.n), N_WORKERS)
    tarefas = [(i, a0[b], e0[b], om0[b], M0[b], SNAPS, args.anos, args.saida)
               for i, b in enumerate(blocos)]
    t0 = time.time()
    with Pool(N_WORKERS) as p:
        tempos = p.map(trabalha, tarefas)
    ws = [np.load(DADOS / f"{args.saida}_w{i}.npz") for i in range(N_WORKERS)]
    np.savez_compressed(
        DADOS / f"{args.saida}_snapshots.npz",
        t=ws[0]["t"],
        a=np.concatenate([w["a"] for w in ws], axis=1),
        e=np.concatenate([w["e"] for w in ws], axis=1),
        vivo_old=np.concatenate([w["vivo_old"] for w in ws], axis=1),
        vivo_marte=np.concatenate([w["vivo_marte"] for w in ws], axis=1),
        a0=a0, e0=e0, semente=SEMENTE, n=args.n, dt=DT, bloco=BLOCO, q_marte=Q_MARTE,
        n_workers=N_WORKERS, tempo_execucao_s=time.time() - t0, e0_sem_dado=sem_dado,
    )
    print(f"fim: {time.time()-t0:.0f}s (workers: {[round(x) for x in tempos]})", flush=True)


if __name__ == "__main__":
    main()
