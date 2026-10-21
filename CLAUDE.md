# astrologia (repositório do Victor, @333victorhugo)

Várias instâncias do Claude trabalham aqui (chat, Claude Code local, cloud). Regras comuns:

- **`genealogia/`**: mapa de relações entre figuras e tradições. Leia `genealogia/CONVENTIONS.md` antes de mexer. Nunca edite `genealogia/data/*.json` à mão: use `python3 genealogia/tools/mapa.py` (idempotente, valida antes de gravar, grava em formato canônico, diffs mínimos).
- O Victor só dá o conteúdo. Cabe a você validar (`mapa.py validate`), regenerar as notas (`mapa.py build`), commitar e dar push no branch de trabalho. Não peça a ele para rodar comandos.
- Fonte conferida antes de entrar no mapa. Sem fonte, não entra; se a tradição afirma sem documento, use `reivindicada`.
- Texto em português do Brasil, sem travessão como pausa.
- **Fontes:** nunca use Wikipedia (nem enciclopédia online parecida) como fonte, para nada no canal. Só livros, artigos científicos e literatura (fontes primárias e edições acadêmicas). Se esbarrar em paywall, avise: o Victor tem muitos livros e pode enviar o que for preciso. Dado que veio de fonte não aceita fica marcado `[FONTE A SUBSTITUIR]` até ser conferido.
