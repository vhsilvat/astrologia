#!/usr/bin/env python3
"""CLI do mapa de relações. Única forma recomendada de alterar data/*.json.

Toda operação é idempotente (rodar duas vezes dá o mesmo resultado), valida o
conjunto inteiro ANTES de gravar e grava em formato canônico (ordem estável,
indentação fixa), de modo que o diff do git só mostra a mudança real.

Uso: python3 tools/mapa.py <comando> [args]   (python3 tools/mapa.py -h)
"""
import argparse, json, pathlib, re, subprocess, sys

DATA = pathlib.Path(__file__).resolve().parent.parent / 'data'
ID_RE = re.compile(r'^[a-z0-9-]+$')


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


class Mapa:
    def __init__(self):
        self.dom = load('domains.json')
        self.rel = load('relacoes.json')
        self.tr = load('trilhas.json')
        self.files = {d['id']: d['file'] for d in self.dom['domains'] if d.get('file')}
        self.D = {k: load(pathlib.Path(f).name) for k, f in self.files.items()}

    # ---- consultas
    def node(self, nid):
        for k, D in self.D.items():
            for n in D['nodes']:
                if n['id'] == nid:
                    return k, n
        return None, None

    def lanes(self):
        return {l['id']: k for k, D in self.D.items() for l in D['lanes']}

    def x(self, y):
        K = self.dom['axis']['knots']
        for a, b in zip(K, K[1:]):
            if a[0] <= y <= b[0]:
                return a[1] + (y - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
        return K[0][1] if y < K[0][0] else K[-1][1]

    def directed(self, t):
        return self.dom['edgeTypes'].get(t, {}).get('directed', True)

    def ekey(self, e):
        a, b = e['from'], e['to']
        if not self.directed(e['type']) and a > b:
            a, b = b, a
        return (a, b, e['type'])

    # ---- validação (espelha a do index.html)
    def validate(self):
        out, seen, lanes = [], set(), self.lanes()
        for k, D in self.D.items():
            for n in D['nodes']:
                i = n['id']
                if not ID_RE.match(i): out.append(f'id fora do padrão: {i}')
                if i in seen: out.append(f'id duplicado: {i}')
                seen.add(i)
                if n['lane'] not in {l['id'] for l in D['lanes']}: out.append(f'{i}: faixa {n["lane"]} não pertence ao tema {k}')
                if n.get('dy') not in (-2, -1, 1, 2): out.append(f'{i}: dy inválido')
                if not isinstance(n.get('yr'), (int, float)): out.append(f'{i}: ano inválido')
                for f in ('name', 'date', 'work', 'why'):
                    if not n.get(f): out.append(f'{i}: falta {f}')
            by = {}
            for n in D['nodes']: by.setdefault(n['lane'], []).append(n)
            for ns in by.values():
                ns = sorted(ns, key=lambda n: self.x(n['yr']))
                for i, a in enumerate(ns):
                    for b in ns[i + 1:]:
                        if self.x(b['yr']) - self.x(a['yr']) >= 84: break
                        if a['dy'] == b['dy']: out.append(f'rótulos podem colidir: {a["id"]} e {b["id"]} (ajuste dy)')
        ek = set()
        for e in self.rel['edges']:
            if e['from'] not in seen or e['to'] not in seen: out.append(f'relação com ponta inexistente: {e["from"]} → {e["to"]}')
            if e['type'] not in self.dom['edgeTypes']: out.append(f'tipo desconhecido: {e["type"]}')
            if e['from'] == e['to']: out.append(f'relação consigo mesmo: {e["from"]}')
            if not e.get('desc'): out.append(f'relação sem descrição: {e["from"]} → {e["to"]}')
            k = self.ekey(e)
            if k in ek: out.append(f'relação duplicada: {k}')
            ek.add(k)
        tid = set()
        for t in self.tr['trails']:
            if t['id'] in tid: out.append(f'trilha duplicada: {t["id"]}')
            tid.add(t['id'])
            for s in t['steps']:
                if s['node'] not in seen: out.append(f'trilha {t["id"]}: nó inexistente {s["node"]}')
        lid = set()
        for L in self.tr['lineages']:
            if L['id'] in lid: out.append(f'linhagem duplicada: {L["id"]}')
            lid.add(L['id'])
            for n in L['nodes']:
                if n not in seen: out.append(f'linhagem {L["id"]}: nó inexistente {n}')
        return out

    # ---- gravação canônica
    def save(self, dry=False):
        errs = self.validate()
        if errs:
            print('NÃO GRAVADO. Problemas:'); [print(' -', e) for e in errs]; sys.exit(1)
        for D in self.D.values():
            D['nodes'].sort(key=lambda n: (n['lane'], n['yr'], n['id']))
        self.rel['edges'].sort(key=lambda e: self.ekey(e))
        outs = {name: obj for name, obj in [('relacoes.json', self.rel), ('trilhas.json', self.tr), ('domains.json', self.dom)]}
        for k, f in self.files.items(): outs[pathlib.Path(f).name] = self.D[k]
        changed = []
        for name, obj in outs.items():
            txt = json.dumps(obj, ensure_ascii=False, indent=1) + '\n'
            p = DATA / name
            if p.read_text(encoding='utf-8') != txt:
                changed.append(name)
                if not dry: p.write_text(txt, encoding='utf-8')
        print(('(simulação) ' if dry else '') + ('alterado: ' + ', '.join(changed) if changed else 'nada a mudar (já estava assim)'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry', action='store_true', help='valida e mostra o que mudaria, sem gravar')
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('validate', help='valida tudo')
    p = sp.add_parser('list', help='lista nodes|edges|trails|lineages|lanes'); p.add_argument('what', choices=['nodes', 'edges', 'trails', 'lineages', 'lanes'])
    p = sp.add_parser('show', help='mostra uma figura e suas relações'); p.add_argument('id')
    p = sp.add_parser('add-node', help='cria ou atualiza (upsert) uma figura')
    for a in ('id', 'domain', 'lane', 'name', 'date', 'work', 'why'): p.add_argument('--' + a, required=a in ('id',))
    p.add_argument('--yr', type=int); p.add_argument('--dy', type=int)
    p = sp.add_parser('rm-node', help='remove figura e tudo que a referencia (relações, passos, linhagens)'); p.add_argument('id')
    p = sp.add_parser('add-edge', help='cria ou atualiza (upsert) relação'); p.add_argument('from_'); p.add_argument('to'); p.add_argument('type'); p.add_argument('desc')
    p = sp.add_parser('rm-edge', help='remove relação (sem tipo: todas entre os dois)'); p.add_argument('from_'); p.add_argument('to'); p.add_argument('type', nargs='?')
    p = sp.add_parser('trail', help='cria ou substitui trilha: id "nome" "intro" passo...  (passo = node|leitura|horas)'); p.add_argument('id'); p.add_argument('name'); p.add_argument('intro'); p.add_argument('steps', nargs='+'); p.add_argument('--default', action='store_true')
    p = sp.add_parser('rm-trail'); p.add_argument('id')
    p = sp.add_parser('lineage', help='cria ou substitui linhagem: id "nome" node...'); p.add_argument('id'); p.add_argument('name'); p.add_argument('nodes', nargs='+')
    p = sp.add_parser('rm-lineage'); p.add_argument('id')
    sp.add_parser('build', help='gera as notas do Obsidian')
    a = ap.parse_args()
    m = Mapa()

    if a.cmd == 'validate':
        errs = m.validate()
        n = sum(len(D['nodes']) for D in m.D.values())
        print(f'{n} nós, {len(m.rel["edges"])} relações, {len(m.tr["trails"])} trilhas, {len(m.tr["lineages"])} linhagens')
        print('OK' if not errs else 'PROBLEMAS:'); [print(' -', e) for e in errs]; sys.exit(1 if errs else 0)
    if a.cmd == 'list':
        if a.what == 'nodes':
            for k, D in m.D.items():
                for n in D['nodes']: print(f'{n["id"]:16} {k:11} {n["lane"]:14} {n["yr"]:>6}  {n["name"]}')
        elif a.what == 'edges':
            for e in m.rel['edges']: print(f'{e["from"]:14} -{e["type"]}-> {e["to"]}')
        elif a.what == 'trails':
            for t in m.tr['trails']: print(t['id'], '|', t['name'], '|', ' > '.join(s['node'] for s in t['steps']))
        elif a.what == 'lineages':
            for L in m.tr['lineages']: print(L['id'], '|', L['name'], '|', ' > '.join(L['nodes']))
        else:
            for k, D in m.D.items():
                for l in D['lanes']: print(k, l['id'], l['name'])
        return
    if a.cmd == 'show':
        k, n = m.node(a.id)
        if not n: sys.exit('inexistente: ' + a.id)
        print(json.dumps(n, ensure_ascii=False, indent=1))
        for e in m.rel['edges']:
            if a.id in (e['from'], e['to']): print(f'  {e["from"]} -{e["type"]}-> {e["to"]}: {e["desc"]}')
        return
    if a.cmd == 'add-node':
        k, n = m.node(a.id)
        if n is None:
            need = [f for f in ('domain', 'lane', 'name', 'date', 'work', 'why', 'yr', 'dy') if getattr(a, f) is None]
            if need: sys.exit('figura nova exige: ' + ', '.join('--' + f for f in need))
            if a.domain not in m.D: sys.exit('tema desconhecido: ' + a.domain)
            n = {'id': a.id}; m.D[a.domain]['nodes'].append(n)
        elif a.domain and a.domain != k:
            sys.exit(f'{a.id} já existe no tema {k}; para mover, remova e recrie (relações serão perdidas, anote-as antes)')
        for f in ('name', 'date', 'yr', 'lane', 'dy', 'work', 'why'):
            if getattr(a, f) is not None: n[f] = getattr(a, f)
        n_ordered = {f: n[f] for f in ('id', 'name', 'date', 'yr', 'lane', 'dy', 'work', 'why') if f in n}
        n.clear(); n.update(n_ordered)
    elif a.cmd == 'rm-node':
        k, n = m.node(a.id)
        if not n: print('já não existe'); return
        m.D[k]['nodes'].remove(n)
        before = len(m.rel['edges'])
        m.rel['edges'] = [e for e in m.rel['edges'] if a.id not in (e['from'], e['to'])]
        for t in m.tr['trails']: t['steps'] = [s for s in t['steps'] if s['node'] != a.id]
        for L in m.tr['lineages']: L['nodes'] = [x for x in L['nodes'] if x != a.id]
        print(f'removido {a.id}; {before - len(m.rel["edges"])} relação(ões) apagada(s)')
    elif a.cmd == 'add-edge':
        e = {'from': a.from_, 'to': a.to, 'type': a.type, 'desc': a.desc}
        key = m.ekey(e)
        for old in m.rel['edges']:
            if m.ekey(old) == key: old.update(desc=a.desc); break
        else: m.rel['edges'].append(e)
    elif a.cmd == 'rm-edge':
        before = len(m.rel['edges'])
        m.rel['edges'] = [e for e in m.rel['edges'] if not (({e['from'], e['to']} == {a.from_, a.to}) and (a.type is None or e['type'] == a.type) and (m.directed(e['type']) is False or (e['from'], e['to']) == (a.from_, a.to)))]
        print(f'{before - len(m.rel["edges"])} relação(ões) removida(s)')
    elif a.cmd == 'trail':
        steps = []
        for s in a.steps:
            try: nd, rd, h = s.split('|'); steps.append({'node': nd, 'read': rd, 'hours': float(h) if '.' in h else int(h)})
            except ValueError: sys.exit('passo inválido (use node|leitura|horas): ' + s)
        t = {'id': a.id, 'name': a.name, 'intro': a.intro, 'steps': steps}
        if a.default:
            for o in m.tr['trails']: o.pop('default', None)
            t['default'] = True
        m.tr['trails'] = [x for x in m.tr['trails'] if x['id'] != a.id] + [t]
    elif a.cmd == 'rm-trail':
        m.tr['trails'] = [x for x in m.tr['trails'] if x['id'] != a.id]
    elif a.cmd == 'lineage':
        m.tr['lineages'] = [x for x in m.tr['lineages'] if x['id'] != a.id] + [{'id': a.id, 'name': a.name, 'nodes': a.nodes}]
    elif a.cmd == 'rm-lineage':
        m.tr['lineages'] = [x for x in m.tr['lineages'] if x['id'] != a.id]
    elif a.cmd == 'build':
        sys.exit(subprocess.call([sys.executable, str(pathlib.Path(__file__).with_name('gerar_obsidian.py'))]))
    m.save(dry=a.dry)


if __name__ == '__main__':
    main()
