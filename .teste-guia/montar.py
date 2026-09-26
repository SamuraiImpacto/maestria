# -*- coding: utf-8 -*-
"""Monta uma pagina que renderiza a aba Guia com os dados REAIS da Erika.

Serve para ver o que ela ve, sem digitar o codigo de ativacao dela em formulario
nenhum. Extrai do app.js so a funcao que desenha o guia e as auxiliares que ela
usa, e chama com o JSON que a edge devolveu.
"""
import io, os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

AQUI = os.path.dirname(os.path.abspath(__file__))
MEMBROS = os.path.join(os.path.dirname(AQUI), "membros")

app = io.open(os.path.join(MEMBROS, "app.js"), encoding='utf-8').read()


def extrair(nome):
    """Pega uma funcao inteira contando chaves, sem cortar vizinhas."""
    m = re.search(r'^(?:function|const|let|var)\s+' + re.escape(nome) + r'\b', app, re.M)
    assert m, "nao achei a funcao %s" % nome
    i = app.index("{", m.start())
    nivel, j = 0, i
    while j < len(app):
        if app[j] == "{":
            nivel += 1
        elif app[j] == "}":
            nivel -= 1
            if nivel == 0:
                break
        j += 1
    return app[m.start():j + 1]


DOLAR = "const $ = (id) => document.getElementById(id);"
pecas = [DOLAR] + [extrair(n) for n in ("esc", "renderizarGuia")]
for n, p in zip(("$ (linha unica)", "esc", "renderizarGuia"), pecas):
    print("extraido %-16s %d caracteres" % (n, len(p)))

dados = io.open(os.path.join(AQUI, "dados-erika.json"), encoding='utf-8').read()

html = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>O que a Erika ve na aba Guia</title>
<link rel="stylesheet" href="../membros/style.css">
<style>body{padding:24px;max-width:900px;margin:0 auto}</style>
</head><body>
<h2 class="view-titulo">Guia das skills</h2>
<div id="guia-skills-lista"></div>
<script src="../membros/guia-skills.js"></script>
<script>
%s
%s
%s
renderizarGuia(%s);
</script>
</body></html>
""" % (pecas[0], pecas[1], pecas[2], dados)

io.open(os.path.join(AQUI, "index.html"), "w", encoding='utf-8').write(html)
print("pagina montada:", os.path.join(AQUI, "index.html"))
