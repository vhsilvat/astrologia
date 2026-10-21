"""Lacunas de Kirkwood: problema restrito planar (Sol, Júpiter, partículas de teste).

Gera ressonancias/dados/kirkwood_snapshots.npz e ressonancias/dados/kirkwood_orbital.npz.
Uso: python kirkwood_sim.py [--anos 2e5] [--n 3000]
"""

import argparse
import time
from pathlib import Path

import numpy as np
import rebound

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"

SEMENTE = 20261021
M_JUPITER = 9.5479e-4
A_JUPITER = 5.2044
E_JUPITER = 0.0489
G = 4.0 * np.pi**2  # UA^3 / (Msol ano^2)
DT = 0.1  # anos
BLOCO = 10.0  # anos entre checagens de ejeção
SNAPS = [0.0, 1e3, 1e4, 5e4, 1e5, 2e5]
N_ANIM, QUADROS, T_ANIM = 500, 600, 50.0


def monta(a, e, om, M):
    sim = rebound.Simulation()
    sim.units = ("yr", "AU", "Msun")
    sim.add(m=1.0)
    sim.add(m=M_JUPITER, a=A_JUPITER, e=E_JUPITER, omega=0.0, M=0.0, primary=sim.particles[0])
    sim.N_active = sim.N
    sim.integrator = "whfast"
    for ai, ei, oi, Mi in zip(a, e, om, M):
        sim.add(m=0.0, a=ai, e=ei, omega=oi, M=Mi, primary=sim.particles[0])
    sim.move_to_com()
    return sim


def estados(sim):
    n = sim.N
    xyz = np.zeros((n, 3))
    vel = np.zeros((n, 3))
    sim.serialize_particle_data(xyz=xyz, vxvyvz=vel)
    return xyz, vel


def elementos_helio(xyz, vel):
    r = xyz[2:, :2] - xyz[0, :2]
    v = vel[2:, :2] - vel[0, :2]
    rn = np.hypot(r[:, 0], r[:, 1])
    v2 = (v**2).sum(axis=1)
    inv_a = 2.0 / rn - v2 / G
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(inv_a > 0, 1.0 / inv_a, np.inf)
    h = r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]
    ex = (v[:, 1] * h) / G - r[:, 0] / rn
    ey = (-v[:, 0] * h) / G - r[:, 1] / rn
    return a, np.hypot(ex, ey), rn


def animacao(a0, e0, om0, M0):
    """Primeiros 50 anos, 500 partículas, 600 quadros (posições heliocêntricas)."""
    sim = monta(a0[:N_ANIM], e0[:N_ANIM], om0[:N_ANIM], M0[:N_ANIM])
    sim.dt = T_ANIM / QUADROS / 2.0
    pos = np.zeros((QUADROS, N_ANIM, 2))
    jup = np.zeros((QUADROS, 2))
    tq = np.linspace(0, T_ANIM, QUADROS, endpoint=False)
    for k, t in enumerate(tq):
        sim.integrate(t)
        xyz, _ = estados(sim)
        pos[k] = xyz[2:, :2] - xyz[0, :2]
        jup[k] = xyz[1, :2] - xyz[0, :2]
    np.savez_compressed(
        DADOS / "kirkwood_orbital.npz", pos=pos, jup=jup, t=tq, a0=a0[:N_ANIM], semente=SEMENTE
    )
    print("animação orbital salva", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anos", type=float, default=2e5)
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--amin", type=float, default=2.0)
    ap.add_argument("--amax", type=float, default=4.2)
    ap.add_argument("--emax", type=float, default=0.1)
    ap.add_argument("--semente", type=int, default=SEMENTE)
    ap.add_argument("--saida", default="kirkwood_snapshots")
    ap.add_argument("--snaps", default="")
    ap.add_argument("--sem-anim", action="store_true")
    args = ap.parse_args()

    rng = np.random.default_rng(args.semente)
    n = args.n
    a0 = rng.uniform(args.amin, args.amax, n)
    e0 = rng.uniform(0.0, args.emax, n)
    om0 = rng.uniform(0, 2 * np.pi, n)
    M0 = rng.uniform(0, 2 * np.pi, n)
    DADOS.mkdir(exist_ok=True)

    snaps_t = [float(x) for x in args.snaps.split(",")] if args.snaps else SNAPS
    if not args.sem_anim:
        animacao(a0, e0, om0, M0)

    # ---- evolução longa ----
    sim = monta(a0, e0, om0, M0)
    sim.dt = DT
    vivo = np.ones(n, dtype=bool)
    a_atual, e_atual = a0.copy(), e0.copy()
    ids = np.arange(n)  # índice original das partículas ainda na simulação
    snap_t, snap_a, snap_e, snap_v = [], [], [], []
    prox = 0
    t = 0.0
    t_ini = time.time()
    tf = args.anos
    while True:
        while prox < len(snaps_t) and snaps_t[prox] <= t + 1e-9 and snaps_t[prox] <= tf:
            snap_t.append(snaps_t[prox])
            snap_a.append(a_atual.copy())
            snap_e.append(e_atual.copy())
            snap_v.append(vivo.copy())
            print(f"t={snaps_t[prox]:.0f} anos, vivas={vivo.sum()}, {time.time()-t_ini:.0f}s", flush=True)
            prox += 1
        if t >= tf - 1e-9:
            break
        t = min(t + BLOCO, tf)
        sim.integrate(t)
        xyz, vel = estados(sim)
        a, e, rn = elementos_helio(xyz, vel)
        a_atual[ids] = a
        e_atual[ids] = e
        ej = (rn < 1.0) | (rn > 10.0) | (e > 0.7) | ~np.isfinite(a)
        if ej.any():
            vivo[ids[ej]] = False
            # remove do fim para o começo para manter índices válidos
            for idx in np.sort(np.where(ej)[0])[::-1]:
                sim.remove(int(idx) + 2)
            ids = ids[~ej]
    np.savez_compressed(
        DADOS / f"{args.saida}.npz",
        t=np.array(snap_t),
        a=np.array(snap_a),
        e=np.array(snap_e),
        vivo=np.array(snap_v),
        a0=a0,
        e0=e0,
        semente=args.semente,
        n=n,
        dt=DT,
        bloco=BLOCO,
        tempo_execucao_s=time.time() - t_ini,
    )
    print(f"fim: {time.time()-t_ini:.0f}s", flush=True)


if __name__ == "__main__":
    main()
