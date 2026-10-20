# A Cadeia de Ouro

Mapa de quem ensinou, influenciou, criticou, identificou ou reivindicou quem, por tema e no tempo (astrologia, mito, cristianismo antigo, alquimia e gnose, psicologia profunda). Apoio de estudo e de roteiro para o canal @333victorhugo.

- `CONVENTIONS.md`: contrato de extensão. Leia primeiro; vale para qualquer instância do Claude.
- `data/`: `domains.json`, um JSON por tema, `relacoes.json` e `trilhas.json`.
- `index.html`: renderizador. Abra com `python3 -m http.server` dentro desta pasta.
- `tools/mapa.py`: CLI para validar, listar, adicionar, alterar e remover (idempotente). `python3 tools/mapa.py -h`.
- `obsidian/`: notas com wikilinks, geradas por `python3 tools/mapa.py build`. Abra como vault e use a visão em grafo.
