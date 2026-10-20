# Genealogia da Astrologia

Mapa de quem ensinou, influenciou, criticou ou reivindicou quem, por tema e no tempo. Serve de apoio de estudo e de roteiro para o canal @333victorhugo.

- `CONVENTIONS.md`: contrato de extensão (leia primeiro, vale para qualquer instância futura do Claude).
- `data/`: `domains.json` (eixo do tempo, tipos de relação, temas) e um JSON por tema (`astrologia.json`, `psicologia.json`).
- `index.html`: renderizador. Abrir com `python3 -m http.server` dentro desta pasta.
- `obsidian/`: notas geradas com wikilinks. Abra esta pasta como vault, ou copie para o seu vault, e use a visão em grafo.
- `tools/gerar_obsidian.py`: regenera `obsidian/` a partir dos JSON.
