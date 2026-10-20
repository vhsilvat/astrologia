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
edges = json.loads((DATA / "relacoes.json").read_text(encoding="utf-8"))["edges"]
tr = json.loads((DATA / "trilhas.json").read_text(encoding="utf-8"))
nodes, lanes, doms = {}, {}, []
trails = tr["trails"]
for d in dom["domains"]:
    if d["status"] != "ativo" or not d.get("file"): continue
    D = json.loads((ROOT / d["file"]).read_text(encoding="utf-8"))
    doms.append(d)
    for l in D["lanes"]: lanes[l["id"]] = dict(l, dom=d)
    for n in D["nodes"]: nodes[n["id"]] = dict(n, dom=d)

names = {}
for i, n in nodes.items():
    f = safe(n["name"])
    assert f not in names.values(), f"nome duplicado: {f}"
    names[i] = f

if OUT.exists(): shutil.rmtree(OUT)
(OUT / "pessoas").mkdir(parents=True)

def link(i): return f"[[{names[i]}]]"

for i, n in nodes.items():
    dr = lambda e: types[e["type"]].get("directed", True)
    inn = [e for e in edges if dr(e) and e["to"] == i]
    out = [e for e in edges if dr(e) and e["from"] == i]
    eq = [e for e in edges if not dr(e) and i in (e["from"], e["to"])]
    L = ["---", f"id: {i}", f"tema: {n['dom']['id']}", f"faixa: {n['lane']}",
         f"ano: {n['yr']}", f"data: \"{n['date']}\"",
         f"tags: [genealogia, {n['dom']['id']}]", "---", "",
         f"# {n['name']}", "", f"*{n['date']} · {n['dom']['name']} · {lanes[n['lane']]['name']}*", "",
         "## Obra", n["work"], "", "## Por que importa", n["why"], ""]
    for t, T in types.items():
        blocks = ([(T.get("out", T["label"]), [e for e in edges if e["type"] == t and e["from"] == i], "to"),
                   (T.get("in", T["label"]), [e for e in edges if e["type"] == t and e["to"] == i], "from")]
                  if dr(e={"type": t}) else
                  [(T.get("out", T["label"]), [e for e in edges if e["type"] == t and i in (e["from"], e["to"])], None)])
        for title, es, key in blocks:
            if not es: continue
            L += [f"## {title}"]
            L += [f"- {link(e[key] if key else (e['to'] if e['from'] == i else e['from']))} · {e['desc']}" for e in es]
            L += [""]
    (OUT / "pessoas" / f"{names[i]}.md").write_text("\n".join(L), encoding="utf-8")

M = ["---", "tags: [genealogia, moc]", "---", "", f"# {dom['title']}", "",
     "Mapa de conteúdo gerado de `genealogia/data/*.json`. Não edite as notas à mão: edite os JSON e rode `python3 genealogia/tools/mapa.py build`.", "",
     "Use a visão em grafo do Obsidian (filtro `tag:#genealogia`) para ver as ligações.", ""]
for d in doms:
    M += [f"## {d['name']}", ""]
    for l in [l for l in lanes.values() if l["dom"]["id"] == d["id"]]:
        ns = sorted([n for n in nodes.values() if n["lane"] == l["id"]], key=lambda n: n["yr"])
        M += [f"### {l['name']}", ""] + [f"- {link(n['id'])} · {n['date']}" for n in ns] + [""]
for t in trails:
    M += [f"## Trilha: {t['name']}", "", t.get("intro", ""), ""]
    M += [f"{k}. {link(s['node'])} · {s['read']} · ~{s['hours']} h" for k, s in enumerate(t["steps"], 1)] + [""]
M += ["## Linhagens", ""]
for L_ in tr["lineages"]:
    M += [f"- **{L_['name']}**: " + " → ".join(link(x) for x in L_["nodes"])]
(OUT / "Genealogia.md").write_text("\n".join(M), encoding="utf-8")
print(f"{len(nodes)} notas, {len(edges)} relações, {len(trails)} trilha(s)")
