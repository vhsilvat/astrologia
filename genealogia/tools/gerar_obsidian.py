#!/usr/bin/env python3
"""Gera notas Markdown (wikilinks) para o Obsidian a partir de data/*.json.
Fonte da verdade: os JSON. Rodar de novo sobrescreve genealogia/obsidian/ (idempotente).
Uso: python3 genealogia/tools/gerar_obsidian.py
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "obsidian"

def safe(n): return re.sub(r'[\\/:*?"<>|#^\[\]]', "", n).strip()

dom = json.loads((DATA / "domains.json").read_text(encoding="utf-8"))
types = dom["edgeTypes"]
nodes, lanes, edges, trails, doms = {}, {}, [], [], []
for d in dom["domains"]:
    if d["status"] != "ativo" or not d.get("file"): continue
    D = json.loads((ROOT / d["file"]).read_text(encoding="utf-8"))
    doms.append(d)
    for l in D["lanes"]: lanes[l["id"]] = dict(l, dom=d)
    for n in D["nodes"]: nodes[n["id"]] = dict(n, dom=d)
    edges += D["edges"]
    for t in D.get("trails", []): trails.append((d, t))

names = {}
for i, n in nodes.items():
    f = safe(n["name"])
    assert f not in names.values(), f"nome duplicado: {f}"
    names[i] = f

if OUT.exists(): shutil.rmtree(OUT)
(OUT / "pessoas").mkdir(parents=True)

def link(i): return f"[[{names[i]}]]"

for i, n in nodes.items():
    inn = [e for e in edges if e["to"] == i]
    out = [e for e in edges if e["from"] == i]
    L = ["---", f"id: {i}", f"tema: {n['dom']['id']}", f"faixa: {n['lane']}",
         f"ano: {n['yr']}", f"data: \"{n['date']}\"",
         f"tags: [genealogia, {n['dom']['id']}]", "---", "",
         f"# {n['name']}", "", f"*{n['date']} · {n['dom']['name']} · {lanes[n['lane']]['name']}*", "",
         "## Obra", n["work"], "", "## Por que importa", n["why"], ""]
    for title, es, key in (("Vem de", inn, "from"), ("Leva a ou atinge", out, "to")):
        L += [f"## {title}"]
        L += [f"- {link(e[key])} · *{types[e['type']]['label']}* · {e['desc']}" for e in es] or ["- (nenhuma registrada)"]
        L += [""]
    (OUT / "pessoas" / f"{names[i]}.md").write_text("\n".join(L), encoding="utf-8")

M = ["---", "tags: [genealogia, moc]", "---", "", "# Genealogia da Astrologia", "",
     "Mapa de conteúdo gerado de `genealogia/data/*.json`. Não edite as notas à mão: edite os JSON e rode `python3 genealogia/tools/gerar_obsidian.py`.", "",
     "Use a visão em grafo do Obsidian (filtro `tag:#genealogia`) para ver as ligações.", ""]
for d in doms:
    M += [f"## {d['name']}", ""]
    for l in [l for l in lanes.values() if l["dom"]["id"] == d["id"]]:
        ns = sorted([n for n in nodes.values() if n["lane"] == l["id"]], key=lambda n: n["yr"])
        M += [f"### {l['name']}", ""] + [f"- {link(n['id'])} · {n['date']}" for n in ns] + [""]
for d, t in trails:
    M += [f"## Trilha: {t['name']}", "", t.get("intro", ""), ""]
    M += [f"{k}. {link(s['node'])} · {s['read']} · ~{s['hours']} h" for k, s in enumerate(t["steps"], 1)] + [""]
(OUT / "Genealogia.md").write_text("\n".join(M), encoding="utf-8")
print(f"{len(nodes)} notas, {len(edges)} relações, {len(trails)} trilha(s)")
