"""Gera a página do teste grátis de cada área a partir de uma base só.

Uso:  python _ferramentas/gerar_teste_areas.py

Entradas:
  _ferramentas/teste-base.html  a página do teste de previdenciário, como foi aprovada
  _ferramentas/areas.json       título, frase e ferramentas de cada área
  <area>/index.html             a página de venda de cada pacote, de onde saem as demonstrações

Saídas:
  teste/index.html              todas as áreas: o vídeo na primeira dobra e a ficha com a escolha da área
                                (endereço divulgado como "o teste", desde 25/11/2026)
  teste/nicho/<area>.html       o miolo de cada área (demonstrações, comparação, conta), que a /teste/
                                troca na hora quando a pessoa escolhe a área na ficha
  teste/<area>/index.html       só redirecionam para /teste/?a=<area>, com a área já marcada
                                (25/11/2026, ordem do Samurai: um endereço só; a área escolhida muda o resto da página)
  teste/area/index.html         redirecionamento do endereço antigo

Nenhum conteúdo jurídico é escrito aqui: petição, cálculo e jurisprudência de cada área
vêm prontos da página do pacote, que já foi conferida quando foi publicada.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
FERR = RAIZ / "_ferramentas"
BASE = (FERR / "teste-base.html").read_text(encoding="utf-8").replace("\r\n", "\n")
AREAS = json.loads((FERR / "areas.json").read_text(encoding="utf-8"))

ORDEM = ["prev", "trab", "familia", "consumidor", "bancario", "criminal", "imobiliario", "empresarial"]
# De qual página de venda sai a demonstração de cada área, e para onde vai quem quer comprar direto.
FONTE = {"trab": "trab-marketing", "familia": "familia", "consumidor": "consumidor", "bancario": "bancario",
         "criminal": "criminal", "imobiliario": "imobiliario", "empresarial": "empresarial"}
SO_A_AREA = {"prev": "/prev/", "trab": "/trab/"}
COM_JURIMETRIA = {"prev", "trab"}
COMUNS = [["Petição no seu timbrado", "Escrita do jeito do seu escritório, com um revisor treinado nos seus critérios."],
          ["Fonte conferida", "Lei, súmula e decisão passam pela fonte oficial antes de entrar na peça. O que não existe, ela joga fora."]]


def troca(h, velho, novo, vezes=1):
    achou = h.count(velho)
    assert achou == vezes, f"esperava {vezes}, achei {achou}: {velho[:70]!r}"
    return h.replace(velho, novo)


def secao(h, sid):
    m = re.search(r'<section[^>]*id="%s"[^>]*>' % sid, h)
    assert m, sid
    return h[m.start():h.index("</section>", m.start()) + len("</section>")]


def caminho(a):
    return f"/teste/{a}/"


def minuscula(s):
    return s[0].lower() + s[1:]


# ---------------------------------------------------------------- estrutura (todas as áreas)
CSS = """
  /* Barra de áreas e formulário na primeira dobra (21/11/2026) */
  .areas-barra{position:relative;z-index:2;max-width:1180px;margin:0 auto 26px;padding:0 24px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center}
  .areas-barra .rot{font-weight:800;font-size:14px;color:var(--muted);margin-right:6px}
  .areas-barra a{font-size:14px;font-weight:700;padding:8px 14px;border-radius:999px;border:1px solid var(--line-strong);color:inherit;text-decoration:none;background:rgba(255,255,255,.03);transition:border-color .2s,background .2s}
  .areas-barra a:hover{border-color:var(--red)}
  .areas-barra a.on{background:var(--red);border-color:var(--red);color:#fff}
  header.hero .teste-form{position:static;margin-top:30px}
  header.hero .teste-form,header.hero .teste-form h3,header.hero .teste-form p,header.hero .teste-form label{text-align:left}
  header.hero .teste-form .btn{justify-content:center;text-align:center}
  .term-faixa{padding:34px 0 0}
  .term-faixa .term{max-width:860px;margin:0 auto}
  @media(min-width:981px){header.hero .teste-form{margin-top:0}}
  @media(max-width:980px){header.hero .eyebrow,header.hero .hero-cta,header.hero .hero-fatos,header.hero .hero-prova{display:none}header.hero h1.big{margin-top:0}header.hero .teste-form{max-width:520px;margin:22px auto 0}}
  @media(max-width:560px){.areas-barra{gap:6px;padding:0 16px;margin-bottom:18px}.areas-barra .rot{width:100%;text-align:center;margin:0 0 2px}.areas-barra a{font-size:13px;padding:6px 11px}}
  @media(prefers-reduced-motion:reduce){.areas-barra a{transition:none}}
"""

JS_FORM = r"""<script>
(function () {
  var EDGE = "https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1/teste-gratis";
  var AREA = "__AREA__";
  var celular = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || "");
  // De onde a pessoa veio: /teste/?o=evento, ?o=grupo-melissa...
  var origem = "site";
  try { origem = (new URLSearchParams(location.search).get("o") || "site").slice(0, 60); } catch (e) {}

  // A barra de áreas leva junto o que veio no endereço (origem e campanha).
  try {
    if (location.search) {
      [].slice.call(document.querySelectorAll(".areas-barra a")).forEach(function (a) { a.href = a.getAttribute("href") + location.search; });
    }
  } catch (e) {}

  // Contador: avisa que a página foi aberta e, depois, que a pessoa começou a preencher.
  // Não manda nome nem e-mail: só a origem e um código sorteado neste navegador.
  var local = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  var visitante = "";
  try {
    visitante = localStorage.getItem("maestria-teste-visitante") || "";
    if (!visitante) { visitante = Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10); localStorage.setItem("maestria-teste-visitante", visitante); }
  } catch (e) {}
  function contar(evento) {
    if (local) return;
    try {
      fetch(EDGE, { method: "POST", keepalive: true, headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ acao: "visita", evento: evento, origem: origem, visitante: visitante }) }).catch(function () {});
    } catch (e) {}
  }
  contar("visita");
  var comecou = false;

  // A página tem dois formulários iguais: o do topo e o do fim. O sufixo separa os campos.
  function ligar(s) {
    var f = document.getElementById("f" + s);
    if (!f) return;
    function g(id) { return document.getElementById(id + s); }
    var erro = g("erro"), btn = g("enviar"), btnTxt = g("enviar-txt"), zap = g("whatsapp");
    f.addEventListener("input", function () { if (!comecou) { comecou = true; contar("formulario"); } });
    zap.addEventListener("input", function () {
      var d = zap.value.replace(/\D/g, "").slice(0, 11);
      zap.value = d.length > 6 ? "(" + d.slice(0, 2) + ") " + d.slice(2, d.length - 4) + "-" + d.slice(-4)
        : d.length > 2 ? "(" + d.slice(0, 2) + ") " + d.slice(2) : d;
    });
    function mostrarErro(msg) { erro.textContent = msg; erro.classList.remove("tf-oculto"); }
    function carregando(sim) {
      btn.disabled = sim; btn.classList.toggle("carregando", sim);
      btnTxt.textContent = sim ? "Liberando o seu teste..." : "Quero testar por 7 dias";
    }
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      erro.classList.add("tf-oculto");
      var dados = {
        nome: g("nome").value.trim(),
        email: g("email").value.trim(),
        whatsapp: zap.value, area: AREA,
        site: g("site").value, origem: origem
      };
      if (dados.nome.length < 3) return mostrarErro("Escreva o seu nome completo.");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(dados.email)) return mostrarErro("Confira o e-mail: ele parece incompleto.");
      if (zap.value.replace(/\D/g, "").length < 10) return mostrarErro("Confira o WhatsApp, com DDD.");
      carregando(true);
      fetch(EDGE, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dados) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          carregando(false);
          j = j || {};
          if (!j.ok) return mostrarErro(j.erro || "Não consegui liberar agora. Tente de novo em instantes.");
          // Cadastro feito: avisa o pixel, para a campanha otimizar por quem libera o teste.
          try { if (window.fbq && j.token) fbq("track", "Lead", { content_name: "Teste 7 dias MaestrIA", content_category: origem }); } catch (e) {}
          // Guarda o acesso desta aba: a área de membros abre já logada, sem digitar nada.
          if (j.token) { try { sessionStorage.setItem("maestria_membros", JSON.stringify({ token: j.token, cpf: j.contato || dados.email })); } catch (e) {} }
          var ate = j.vence_em ? new Date(j.vence_em).toLocaleDateString("pt-BR") : "";
          var pacote = j.plano_legivel ? j.plano_legivel + ", até " + ate + ". " : "Vale até " + ate + ". ";
          g("ok-titulo").textContent = (j.nome ? j.nome + ", o" : "O") + " seu teste está liberado!";
          if (celular) {
            g("ok-texto").textContent = pacote + "A instalação é no computador: abra lá o e-mail que acabamos de mandar e clique no botão azul.";
            g("ok-btn").classList.add("tf-oculto");
          } else {
            g("ok-texto").textContent = pacote + "Agora é só instalar: a próxima tela mostra cada passo e onde clicar.";
          }
          g("tela-form").classList.add("tf-oculto");
          g("tela-ok").classList.remove("tf-oculto");
          g("cartao").scrollIntoView({ block: "center" });
        })
        .catch(function () { carregando(false); mostrarErro("Sem conexão agora. Confira a internet e tente de novo."); });
    });
  }
  ligar("");
  ligar("2");
})();
</script>"""


def estrutura(h, a):
    nome = AREAS[a]["nome"]
    # 1. terminal sai do topo e o formulário entra no lugar
    i = h.index('    <div class="term" id="term">')
    f = h.index("\n  </div>\n</header>", i)
    term = h[i:f].rstrip()
    ci = h.index('      <div class="teste-form reveal" id="cartao">')
    cf = h.index('      <div class="teste-inclui reveal">', ci)
    cartao = h[ci:cf].rstrip()
    cartao = troca(cartao, "também no seu WhatsApp.</p>", f"também no seu WhatsApp. Você testa <b>{nome} + Marketing</b>.</p>")
    segundo = re.sub(r'\b(id|for)="([\w-]+)"', lambda m: f'{m.group(1)}="{m.group(2)}2"', cartao)
    topo = cartao.replace('class="teste-form reveal"', 'class="teste-form"')
    h = h[:ci] + segundo + "\n" + h[cf:]
    h = h[:i] + topo + h[f:]
    h = troca(h, '<section id="funcoes">', '<section class="term-faixa">\n  <div class="wrap">\n' + term + '\n  </div>\n</section>\n\n<section id="funcoes">')
    # 2. barra de áreas
    barra = '  <div class="areas-barra" role="navigation" aria-label="Escolha a sua área"><span class="rot">Qual é a sua área?</span>' + "".join(
        f'<a href="{caminho(x)}"{" class=\"on\" aria-current=\"page\"" if x == a else ""}>{AREAS[x]["nome"]}</a>' for x in ORDEM) + "</div>\n"
    h = troca(h, '<header class="hero" id="topo">\n', '<header class="hero" id="topo">\n' + barra)
    h = troca(h, '<a href="#teste" class="btn btn-red">Quero testar 7 dias grátis</a>', '<a href="#cartao" class="btn btn-red">Quero testar 7 dias grátis</a>')
    # 3. estilos e o envio dos dois formulários
    h = troca(h, "</style>", CSS + "</style>")
    ji = h.index('<script>\n(function () {\n  var EDGE')
    jf = h.index("</script>", ji) + len("</script>")
    h = h[:ji] + JS_FORM.replace("__AREA__", a) + h[jf:]
    h = troca(h, '<meta property="og:url" content="https://maestria.samurailab.com.br/teste/">',
              f'<meta property="og:url" content="https://maestria.samurailab.com.br{caminho(a)}">')
    return h


# ---------------------------------------------------------------- conteúdo (as sete áreas novas)
def conteudo(h, a):
    d = AREAS[a]
    nome = d["nome"]
    fonte = (RAIZ / FONTE[a] / "index.html").read_text(encoding="utf-8").replace("\r\n", "\n")
    h1 = d["h1"].replace("<em>", '<span class="red">').replace("</em>", "</span>")

    h = h.replace("Previdenciário + Marketing", f"{nome} + Marketing")
    h = troca(h, "cálculo do INSS com memória aberta", "cálculo com memória aberta")
    h = troca(h, "Previdenciário e Marketing completos", f"{nome} e Marketing completos")

    # topo
    h = troca(h, '<h1 class="big">A pasta do cliente entra. <span class="red">O caso pronto para protocolar sai.</span></h1>', f'<h1 class="big">{h1}</h1>')
    i = h.index('<p class="hero-sub">')
    h = h[:i] + f'<p class="hero-sub">{d["sub"]} E ela ainda faz o conteúdo do seu Instagram.</p>' + h[h.index("</p>", i) + 4:]
    i = h.index('<p class="hero-prova">')
    f = h.index("</p>", i)
    prova = h[i:f]
    prova = prova[:prova.index("<span><b>")] + "<span><b>Já roda em escritório de verdade, com caso de verdade.</b> Mais abaixo, a palavra de quem usa.</span>"
    h = h[:i] + prova + h[f:]

    # terminal
    linhas = [f'<p class="tl t-cmd"><span class="p">&gt;</span>{minuscula(d["cmd"]).rstrip(".")}</p>']
    linhas += [f'<p class="tl t-resp">{p}</p>' for p in d["passos"][:2]]
    linhas += [f'<p class="tl t-ok">✓ {t}. {x}</p>' for _, t, x in d["arq"]]
    linhas += ['<p class="tl t-cmd"><span class="p">&gt;</span>cria o carrossel da semana do meu Instagram</p>',
               '<p class="tl t-ok">✓ 8 lâminas com a sua marca e a legenda, dentro das regras da OAB</p>',
               '<p class="tl t-dim">Exemplo ilustrativo. O advogado revisa tudo antes de usar.<span class="cursor" id="cur"></span></p>']
    i = h.index('<div class="term-body" id="termbody">') + len('<div class="term-body" id="termbody">')
    f = h.index("</div>", i)
    h = h[:i] + "\n        " + "\n        ".join(linhas) + "\n      " + h[f:]

    # tudo o que ela faz
    cartoes = d["vem"] + COMUNS
    sec = secao(h, "funcoes")
    bi = sec.index('<div class="fx reveal">')
    bf = sec.index('<div class="fx-rot', bi)
    velho = sec[bi:bf]
    icones = re.findall(r'<span class="fx-ic">.*?</span>', velho, flags=re.S)
    assert len(icones) == 9 and velho.count("<div") == velho.count("</div>"), (len(icones), velho.count("<div"), velho.count("</div>"))
    novo = '<div class="fx reveal">\n      <div class="cardy topo">\n        ' + icones[0] + \
        f'\n        <div><h3>Do documento do cliente ao arquivo pronto</h3><p>{d["sub"]} Tudo sai em Word, Excel e PDF, para você revisar e assinar.</p></div>' + \
        f'\n        <div class="fx-pedido"><small>Você escreve</small>{minuscula(d["cmd"]).rstrip(".")}</div>\n      </div>\n' + \
        "".join(f'      <div class="cardy">{icones[k + 1]}<h3>{t}</h3><p>{x}</p></div>\n' for k, (t, x) in enumerate(cartoes)) + "    </div>\n    "
    sec2 = sec[:bi] + novo + sec[bf:]
    sec2 = troca(sec2, '<div class="fx-rot reveal">Previdenciário</div>', f'<div class="fx-rot reveal">{nome}</div>')
    h = troca(h, sec, sec2)

    # quem já usa
    h = troca(h, '<h2 class="sec reveal">Feita e testada por previdenciaristas. <span class="red">Mais de 30 escritórios</span> na fase piloto.</h2>',
              '<h2 class="sec reveal">Quem já usa, <span class="red">com caso de verdade</span>.</h2>')

    # o seu jeito de pedir: botões e roteiros da própria área
    botoes = re.findall(r'data-ac="(\w+)">([^<]+)', fonte)
    mi = BASE.index("      carrossel: {")
    mf = BASE.index("\n    };", mi)
    marketing = BASE[mi:mf]
    ri = fonte.index("var ROTEIROS = {") + len("var ROTEIROS = {")
    corpo = fonte[ri:fonte.index("\n    };", ri)].rstrip()
    if a == "trab":
        escolhidos = botoes
    else:
        escolhidos = botoes[:4] + [("carrossel", "Escrever o carrossel da semana"), ("calendario", "Montar o calendário do mês"),
                                   ("site", "Construir o site do escritório"), ("landing", "Criar a página da campanha")]
        marketing = troca(marketing, 'e a persona \\"cliente de aposentadoria\\"... tema: revisão de benefício', "e a persona do seu cliente... tema puxado do calendário do mês")
        corpo = corpo.rstrip(",") + ",\n" + marketing
    for chave, _ in escolhidos:
        assert re.search(r"^\s+%s: \{ titulo" % chave, corpo, flags=re.M), chave
    lista = "".join(f'\n      <button class="acao{" on" if k == 0 else ""}" data-ac="{c}">{r}<i>›</i></button>' for k, (c, r) in enumerate(escolhidos))
    i = h.index('<div class="acoes-lista reveal">') + len('<div class="acoes-lista reveal">')
    f = h.index("\n    </div>", i)
    h = h[:i] + lista + h[f:]
    i = h.index("var ROTEIROS = {") + len("var ROTEIROS = {")
    f = h.index("\n    };", i)
    h = h[:i] + corpo + h[f:]
    h = troca(h, "rodarRoteiro('calculo')", f"rodarRoteiro('{escolhidos[0][0]}')")
    h = troca(h, "// ACOES: cada botao roda um roteiro previdenciario completo, linha a linha", "// ACOES: cada botao roda um roteiro completo, linha a linha")

    # as quatro demonstrações jurídicas, vindas da página do pacote
    ids = re.findall(r'<section[^>]*id="([^"]+)"', fonte)
    quatro = ["peticao", "calculo", ids[ids.index("calculo") + 1], "juris"]
    assert ids.index("juris") == ids.index("calculo") + 2, ids
    bloco = "\n\n".join(secao(fonte, s) for s in quatro)
    bloco = re.sub(r'(<section id="peticao")[^>]*>', r'\1 style="padding-top:56px">', bloco, count=1)
    i = h.index('<section id="peticao"')
    f = h.index("</section>", h.index('<section id="juris"')) + len("</section>")
    h = h[:i] + bloco + h[f:]
    h = troca(h, "Parte 1 · Previdenciário", f"Parte 1 · {nome}")
    # no trabalhista, a página de venda também traz os exemplos de marketing da área
    if a == "trab":
        mkt = ["conteudo", "calendario", "compliance", "voz", "seu"]
        bloco_mkt = "\n\n".join(secao(fonte, s) for s in mkt)
        bloco_mkt = re.sub(r'(<section id="conteudo")[^>]*>', r'\1 style="padding-top:56px">', bloco_mkt, count=1)
        i = h.index('<section id="conteudo"')
        f = h.index("</section>", h.index('<section id="seu"')) + len("</section>")
        h = h[:i] + bloco_mkt + h[f:]
        bloco += bloco_mkt
    # o que veio de outra página precisa ter estilo nesta
    css = BASE[BASE.index("<style>"):BASE.index("</style>")]
    sem_estilo = sorted(c for c in set(x for g in re.findall(r'class="([^"]+)"', bloco) for x in g.split()) if not re.search(r"\.%s\b" % re.escape(c), css))
    assert not sem_estilo, (a, sem_estilo)

    # comparação com a IA comum e a conta
    h = troca(h, "não tem o motor de cálculo do INSS", "não tem o motor de cálculo da sua área")
    h = troca(h, "<span>Calcular o auxílio-acidente</span>", "<span>Fazer o cálculo do caso</span>")
    h = troca(h, "Lê a carta de concessão, calcula com <b>motor testado</b> e os reajustes oficiais do INSS e entrega o Excel com a memória aberta, mês a mês.",
              "Lê os documentos do caso, calcula com <b>motor testado</b> e entrega o Excel com a memória aberta, linha a linha.")
    h = troca(h, "<b>Cálculo previdenciário feito na mão</b>", "<b>Cálculo do caso feito na mão</b>")
    if a not in COM_JURIMETRIA:
        i = h.index('<div class="vs-row" role="row"><div class="tema" role="cell"><span>Escolher onde entrar com a ação</span>')
        h = h[:i] + h[h.index('<div class="vs-row"', i + 10):]
        i = h.index('<div class="conta-l"><div><b>Plataforma de jurimetria</b>')
        h = h[:i] + h[h.index('<div class="conta-l"', i + 10):]
        h = troca(h, '<div class="v">R$ 16 a 41 mil</div>', '<div class="v">R$ 13 a 38 mil</div>')
    # o preço do pacote com o Marketing precisa bater com a página de venda
    assert "R$ 997" in secao(fonte, "pacotes"), a

    # o que entra no teste
    i = h.index('<div class="h">Previdenciário</div>')
    f = h.index("</ul>", i) + len("</ul>")
    itens = "".join(f'\n            <li><span class="ck">✓</span><span><b>{t}:</b> {minuscula(x).rstrip(".")}</span></li>' for t, x in cartoes)
    h = h[:i] + f'<div class="h">{nome}</div>\n        <ul>{itens}\n        </ul>' + h[f:]

    # compra direta e rodapé
    h = troca(h, 'href="/prev-marketing/#pacotes"', f'href="/{FONTE[a]}/#pacotes"')
    h = troca(h, '<a href="/prev/">Só o Previdenciário</a>', f'<a href="{SO_A_AREA.get(a, "/" + FONTE[a] + "/")}">Só o {nome}</a>')
    return h


REDIRECIONA = """<!DOCTYPE html>
<html lang="pt-BR">
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<title>Teste a MaestrIA por 7 dias</title>
<script>
(function () {
  // Endereço antigo do teste por área. Leva para a página única, mantendo a área e a origem.
  var areas = { prev: 1, trab: 1, familia: 1, consumidor: 1, bancario: 1, criminal: 1, imobiliario: 1, empresarial: 1 };
  var p = new URLSearchParams(location.search), a = (p.get("a") || "").toLowerCase();
  p.delete("a");
  var resto = p.toString();
  location.replace("/teste/" + (areas[a] ? a + "/" : "") + (resto ? "?" + resto : ""));
})();
</script>
<noscript><meta http-equiv="refresh" content="0;url=/teste/"></noscript>
<p style="font-family:sans-serif;padding:24px">Abrindo o teste da MaestrIA. Se não abrir, <a href="/teste/">toque aqui</a>.</p>
</html>
"""

# ---------------------------------------------------------------- /teste/: todas as áreas (25/11/2026)
# Pedido do Samurai: o endereço /teste/ foi divulgado como o teste de todas as áreas. A primeira dobra
# é só o título, o vídeo e o botão; o botão desce para a ficha, onde a pessoa escolhe a área.
CSS_TODOS = """
  /* primeira dobra com o vídeo: título, vídeo e botão numa tela só */
  header.hero.hero-vsl{padding:18px 0 22px;min-height:calc(100svh - 64px);display:flex;align-items:center}
  header.hero.hero-vsl .wrap{display:flex;flex-direction:column;align-items:center;text-align:center;gap:0;width:100%}
  header.hero.hero-vsl .hero-art{opacity:.14!important}
  header.hero.hero-vsl h1.big{font-size:clamp(1.7rem,2.7vw,2.6rem);line-height:1.08;max-width:32ch;margin:12px auto 0}
  .hero-vsl .hv-sub{margin:10px auto 0;max-width:60ch;color:var(--muted);font-size:clamp(.98rem,1.15vw,1.08rem);line-height:1.5}
  .hv-video{position:relative;margin:18px auto 0;width:min(100%,1000px,calc((100svh - 64px - 365px) * 16 / 9));min-width:min(100%,480px);aspect-ratio:16/9;border-radius:16px;overflow:hidden;
    border:1px solid rgba(239,39,39,.55);box-shadow:0 0 0 6px rgba(239,39,39,.07),0 30px 80px -30px rgba(239,39,39,.45);
    background:linear-gradient(100deg,#141417 30%,#1d1d22 50%,#141417 70%);background-size:300% 100%;animation:hvbrilho 1.6s linear infinite}
  .hv-video.pronto{animation:none;background:#0b0a0a}
  .hv-video video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;background:transparent}
  .hv-play{position:absolute;inset:0;display:flex;flex-direction:row;align-items:flex-end;justify-content:center;gap:14px;padding-bottom:5.5%;border:0;cursor:pointer;color:#fff;
    background:radial-gradient(ellipse at center,rgba(11,10,10,0) 50%,rgba(11,10,10,.92) 92%);font:700 15px var(--sans);letter-spacing:.02em;transition:background .25s}
  .hv-play:hover{background:radial-gradient(ellipse at center,rgba(11,10,10,0) 50%,rgba(11,10,10,.85) 92%)}
  .hv-play:focus-visible{outline:3px solid #fff;outline-offset:-6px}
  .hv-ic{display:inline-flex;width:72px;height:72px;border-radius:50%;background:var(--red);align-items:center;justify-content:center;box-shadow:0 0 0 10px rgba(239,39,39,.22);transition:transform .25s}
  .hv-ic svg{width:30px;height:30px;margin-left:4px}
  .hv-play:hover .hv-ic{transform:scale(1.07)}
  .hv-play span.t{margin-bottom:17px;background:rgba(11,10,10,.78);padding:9px 16px;border-radius:999px}
  .hv-video.tocando .hv-play{display:none}
  .hero-vsl .hv-cta{margin-top:18px;display:flex;flex-direction:column;align-items:center;gap:12px}
  header.hero.hero-vsl .hero-fatos{display:flex}header.hero.hero-vsl .eyebrow{display:inline-flex}
  .hero-vsl .hero-fatos{margin-top:0;justify-content:center}
  .hero-vsl .hv-entra{opacity:0;transform:translateY(14px);animation:hventra .6s cubic-bezier(.2,.7,.2,1) forwards}
  .hero-vsl .hv-entra.d1{animation-delay:.08s}.hero-vsl .hv-entra.d2{animation-delay:.16s}.hero-vsl .hv-entra.d3{animation-delay:.26s}.hero-vsl .hv-entra.d4{animation-delay:.36s}
  @keyframes hventra{to{opacity:1;transform:none}}
  @keyframes hvbrilho{to{background-position:-150% 0}}
  /* a ficha com a escolha da área */
  #teste{scroll-margin-top:12px}
  #area{scroll-margin-top:12px;padding-bottom:10px}
  .seletor-area{border:0;margin:30px auto 0;padding:0;max-width:900px}
  .seletor-area .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .seletor-area .op{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
  .seletor-area label{position:relative;cursor:pointer;display:block}
  .seletor-area input{position:absolute;opacity:0;width:1px;height:1px}
  .seletor-area span{display:flex;align-items:center;justify-content:center;min-height:62px;padding:12px;border-radius:14px;border:1px solid var(--line-strong);background:var(--panel);font-weight:800;font-size:16px;transition:border-color .2s,background .2s,transform .2s}
  .seletor-area label:hover span{border-color:var(--red);transform:translateY(-2px)}
  .seletor-area input:checked+span{background:var(--red);border-color:var(--red);color:#fff;box-shadow:0 14px 40px -18px rgba(239,39,39,.8)}
  .seletor-area input:focus-visible+span{outline:2px solid #fff;outline-offset:3px}
  @media (max-width:700px){.seletor-area .op{grid-template-columns:1fr 1fr;gap:8px}.seletor-area span{min-height:52px;font-size:15px}}
  @media (prefers-reduced-motion:reduce){.seletor-area span{transition:none}.seletor-area label:hover span{transform:none}}
  #nicho.vazio{display:none}
  #nicho{transition:opacity .25s;min-height:60vh}
  #nicho.trocando{opacity:.25;pointer-events:none}
  @media (prefers-reduced-motion:reduce){#nicho{transition:none}}
  .tf-areas{border:0;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
  .tf-areas legend{font-weight:700;font-size:15px;margin-bottom:8px;padding:0}
  .tf-areas .op{display:flex;flex-wrap:wrap;gap:8px}
  .tf-areas label{position:relative;cursor:pointer}
  .tf-areas input{position:absolute;opacity:0;width:1px;height:1px}
  .tf-areas span{display:inline-block;font-size:14px;font-weight:700;padding:8px 13px;border-radius:999px;border:1px solid var(--line-strong);background:rgba(255,255,255,.03);transition:border-color .2s,background .2s}
  .tf-areas label:hover span{border-color:var(--red)}
  .tf-areas input:checked+span{background:var(--red);border-color:var(--red);color:#fff}
  .tf-areas input:focus-visible+span{outline:2px solid #fff;outline-offset:2px}
  .areas-ver{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:34px;text-align:left}
  .areas-ver a{display:block;padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--panel);color:inherit;text-decoration:none;transition:border-color .2s,transform .2s}
  .areas-ver a:hover{border-color:var(--red);transform:translateY(-2px)}
  .areas-ver b{display:block;font-size:16px}
  .areas-ver small{display:block;margin-top:6px;color:var(--red-ink);font-weight:700;font-size:13px}
  @media (max-width:900px){.areas-ver{grid-template-columns:1fr 1fr}}
  @media (max-width:700px){
    header.hero.hero-vsl{min-height:auto;padding-top:14px}
    .hv-video{width:100%;min-width:0;border-radius:12px}
    .hv-ic{width:52px;height:52px}.hv-ic svg{width:22px;height:22px}.hv-play{gap:10px;font-size:13px}.hv-play span.t{padding:7px 12px;margin-bottom:12px}
    .hero-vsl .btn-lg{width:100%}
  }
  @media (prefers-reduced-motion:reduce){.hero-vsl .hv-entra{animation:none;opacity:1;transform:none}.hv-video{animation:none}.hv-ic,.hv-play,.tf-areas span,.areas-ver a{transition:none}}
"""

HERO_VSL = """<header class="hero hero-vsl" id="topo">
  <div class="hero-art" id="heroArt" aria-hidden="true"><img src="/img/logo-sym.png" alt=""></div>
  <div class="wrap">
    <span class="eyebrow hv-entra"><i></i>Teste grátis de 7 dias &nbsp;•&nbsp; Escolha a sua área</span>
    <h1 class="big hv-entra d1">Uma equipe de assistentes jurídicos <span class="red">dentro do seu computador.</span></h1>
    <p class="hv-sub hv-entra d2">Dê o play: em 3 minutos você vê um caso sair da pasta do cliente pronto para protocolar. Você só revisa e assina.</p>
    <div class="hv-video hv-entra d3" id="hvVideo">
      <video id="vsl" preload="none" playsinline poster="/teste/vsl-capa.jpg" src="/teste/vsl-maestria.mp4" aria-label="Vídeo: o que é a MaestrIA, em 3 minutos"></video>
      <button type="button" class="hv-play" id="hvPlay" aria-label="Assistir ao vídeo com som"><span class="hv-ic"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg></span><span class="t">Assistir com som &nbsp;•&nbsp; 3 min</span></button>
    </div>
    <div class="hv-cta hv-entra d4">
      <a href="#area" class="btn btn-red btn-lg">Quero testar 7 dias grátis</a>
      <div class="hero-fatos"><span><b>✓</b> Sem cartão</span><span><b>✓</b> Sem cobrança automática</span><span><b>✓</b> Com os seus casos</span></div>
    </div>
  </div>
</header>"""

JS_VSL = """<script>
(function () {
  var box = document.getElementById("hvVideo"), v = document.getElementById("vsl"), b = document.getElementById("hvPlay");
  if (!box || !v || !b) return;
  var capa = new Image();
  capa.onload = capa.onerror = function () { box.classList.add("pronto"); };
  capa.src = v.getAttribute("poster");
  b.addEventListener("click", function () {
    box.classList.add("tocando"); v.controls = true; v.muted = false;
    var p = v.play(); if (p && p.catch) p.catch(function () { box.classList.remove("tocando"); });
  });
  v.addEventListener("ended", function () {
    var alvo = document.getElementById("area"); if (alvo) alvo.scrollIntoView({ behavior: "smooth" });
  });
})();
</script>"""


def miolo(h):
    m = h[h.index("</header>") + len("</header>"):h.index('<section id="faq"')]
    i = m.index('<section id="teste">')
    m = m[:i] + m[m.index("</section>", i) + len("</section>"):]
    return m.strip()


def scripts_da_pagina(h):
    todos_ = re.findall(r"<script>.*?</script>", h[h.index("</footer>"):], flags=re.S)
    return [x for x in todos_ if "var EDGE" not in x]


JS_NICHO = """<script>
(function () {
  // A área marcada na ficha troca, na hora, tudo o que vem depois dela: demonstrações, comparação e conta.
  var box = document.getElementById("nicho");
  if (!box) return;
  var atual = box.getAttribute("data-area"), cache = {};
  var NOMES = __NOMES__;
  function mostrar(a) {
    box.classList.remove("vazio");
    var n = document.getElementById("area-nome"); if (n && NOMES[a]) n.textContent = NOMES[a];
  }
  function rodarScripts(el) {
    [].slice.call(el.querySelectorAll("script")).forEach(function (s) {
      var n = document.createElement("script"); n.text = s.textContent; s.parentNode.replaceChild(n, s);
    });
  }
  function trocar(a) {
    if (!a) return;
    mostrar(a);
    if (a === atual) return;
    atual = a;
    box.classList.add("trocando");
    box.setAttribute("aria-busy", "true");
    function baixar() {
      // conexão travada não pode deixar a página parada: depois de 6 s, desiste e tenta de novo
      var ctl = window.AbortController ? new AbortController() : null;
      var t = setTimeout(function () { if (ctl) ctl.abort(); }, 6000);
      return fetch("/teste/nicho/" + a + ".html", ctl ? { signal: ctl.signal } : {})
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (x) { clearTimeout(t); return x; }, function (e) { clearTimeout(t); throw e; });
    }
    // se a rede falhar, tenta de novo uma vez antes de desistir
    var pega = cache[a] ? Promise.resolve(cache[a]) : baixar().catch(function () { return new Promise(function (ok) { setTimeout(ok, 800); }).then(baixar); });
    pega.then(function (t) {
      cache[a] = t;
      if (atual !== a) return;
      box.innerHTML = t;
      box.setAttribute("data-area", a);
      rodarScripts(box);
      box.classList.remove("trocando");
      box.removeAttribute("aria-busy");
    }).catch(function () {
      atual = box.getAttribute("data-area");
      box.classList.remove("trocando");
      box.removeAttribute("aria-busy");
    });
    try { var u = new URL(location.href); u.searchParams.set("a", a); history.replaceState(null, "", u); } catch (e) {}
  }
  document.addEventListener("change", function (e) {
    if (!e.target || e.target.name !== "area") return;
    trocar(e.target.value);
    var t = document.getElementById("nicho");
    if (t) setTimeout(function () { t.scrollIntoView({ behavior: "smooth" }); }, 150);
  });
  var marcada = document.querySelector('input[name="area"]:checked');
  if (marcada) trocar(marcada.value);
})();
</script>"""


def todos(h):
    cabeca = h[:h.index("<nav>")]
    cabeca = re.sub(r"<title>.*?</title>", "<title>Teste a MaestrIA por 7 dias, na sua área</title>", cabeca)
    cabeca = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Teste por 7 dias, sem cartão, a MaestrIA da sua área com o Marketing: petição no seu timbrado, cálculo com memória aberta, jurisprudência conferida e conteúdo com a sua voz. Roda no seu computador, dentro do Claude.">', cabeca)
    cabeca = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Teste a MaestrIA por 7 dias, na sua área">', cabeca)
    cabeca = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="A sua área e o Marketing completos, no seu computador, por 7 dias. Você só decide depois de usar.">', cabeca)
    cabeca = cabeca.replace('content="https://maestria.samurailab.com.br/teste/prev/"', 'content="https://maestria.samurailab.com.br/teste/"')
    cabeca = troca(cabeca, "</style>", CSS_TODOS + "</style>")

    nav = h[h.index("<nav>"):h.index("</nav>") + len("</nav>")]
    i = nav.index('<div class="nav-links">')
    f = nav.index("</div>", i) + len("</div>")
    nav = nav[:i] + '''<div class="nav-links">
      <a href="#topo">Assista</a>
      <a href="#faq">Perguntas</a>
      <a href="#area" class="btn btn-red btn-sm nav-cta">Testar 7 dias grátis</a>
    </div>''' + nav[f:]

    # a ficha: a mesma do topo das páginas por área, com a escolha da área no começo
    ci = h.index('<div class="teste-form" id="cartao">')
    cf = h.index("\n  </div>\n</header>", ci)
    cartao = h[ci:cf].rstrip()
    cartao = troca(cartao, "Você testa <b>Previdenciário + Marketing</b>.", 'Você testa <b><span id="area-nome">a sua área</span> + Marketing</b>.')
    secao_area = '''<section id="area">
  <div class="wrap sec-center">
    <span class="kicker reveal"><span>Para começar</span></span>
    <h2 class="sec reveal">Escolha a sua área e teste <span class="red">por 7 dias, sem pagar nada</span>.</h2>
    <p class="lead reveal">A página se ajusta à sua área: logo abaixo você vê o que ela faz no seu dia a dia. O cadastro do teste fica no fim.</p>
    <fieldset class="seletor-area reveal"><legend class="sr">Qual é a sua área?</legend><div class="op">''' + "".join(
        f'<label><input type="radio" name="area" value="{x}"><span>{AREAS[x]["nome"]}</span></label>' for x in ORDEM) + '''</div></fieldset>
  </div>
</section>'''
    li = lambda t: f'<li><span class="ck">✓</span><span>{t}</span></li>'
    secao_teste = f'''<section id="teste">
  <div class="wrap sec-center">
    <span class="kicker reveal"><span>Liberar o teste</span></span>
    <h2 class="sec reveal">Gostou do que viu? <span class="red">Teste por 7 dias, sem pagar nada.</span></h2>
    <p class="lead reveal">Não é uma versão reduzida nem uma demonstração com caso inventado. É a ferramenta inteira da sua área, com o Marketing junto, no seu computador.</p>
    <div class="teste-grade">
      {cartao}
      <div class="teste-inclui reveal">
        <div class="h">O que vem no teste</div>
        <ul>
          {li("<b>A ferramenta completa da sua área:</b> petição no seu timbrado, cálculo com memória aberta e jurisprudência conferida em fonte oficial")}
          {li("<b>O Marketing junto:</b> carrossel, calendário do mês, roteiro de vídeo e legenda, com a sua voz e dentro das regras da OAB")}
          {li("<b>Com os seus casos:</b> os arquivos ficam em pastas suas, no seu computador")}
          {li("<b>Instalação guiada:</b> imagem de cada tela e suporte no grupo da comunidade")}
          {li("<b>Sem cartão:</b> no fim dos 7 dias o teste pausa sozinho, e você decide")}
        </ul>
      </div>
    </div>
  </div>
</section>'''
    secao_areas = '''<section id="areas" style="padding-top:0">
  <div class="wrap sec-center">
    <h2 class="sec reveal">Quer ver antes o que ela faz <span class="red">na sua área</span>?</h2>
    <p class="lead reveal">Cada área tem a sua página, com as demonstrações de petição, cálculo e jurisprudência.</p>
    <div class="areas-ver reveal">''' + "".join(
        f'\n      <a href="{caminho(x)}"><b>{AREAS[x]["nome"]}</b><small>Ver o teste de {AREAS[x]["nome"]} ›</small></a>' for x in ORDEM) + '''
    </div>
  </div>
</section>'''

    faq = h[h.index('<section id="faq"'):h.index("</section>", h.index('<section id="faq"')) + len("</section>")]
    faq = troca(faq, "O pacote Previdenciário + Marketing custa R$ 997 por 12 meses, com as atualizações do período.",
                "O pacote da sua área com o Marketing custa R$ 997 por 12 meses, com as atualizações do período.")
    final = h[h.index('<section class="final">'):h.index("</section>", h.index('<section class="final">')) + len("</section>")]
    final = re.sub(r'\n    <p class="reveal" style="margin-top:16px;font-size:15px">Já decidiu.*?</p>', "", final)
    final = troca(final, "<span>Os dois pacotes completos</span>", "<span>A sua área + o Marketing</span>")
    final = troca(final, '<a href="#teste" class="btn btn-red btn-lg reveal">', '<a href="#area" class="btn btn-red btn-lg reveal">')
    rodape = h[h.index("<footer>"):h.index("</footer>") + len("</footer>")]
    rodape = troca(rodape, '<a href="/prev/">Só o Previdenciário</a><a href="/marketing/">Só o Marketing</a>', '<a href="/">Todas as áreas</a><a href="/marketing/">Só o Marketing</a>')

    scripts = re.findall(r"<script>.*?</script>", h[h.index("</footer>"):], flags=re.S)
    js_form = JS_FORM.replace("__AREA__", "")
    js_form = troca(js_form, 'var AREA = "";', '''var AREA = "";
  function areaEscolhida() { var r = document.querySelector('input[name="area"]:checked'); return r ? r.value : ""; }
  // Quem chega com ?a=trab já encontra a área marcada.
  try {
    var pa = (new URLSearchParams(location.search).get("a") || "").toLowerCase();
    var marca = pa && document.querySelector('input[name="area"][value="' + pa.replace(/[^a-z]/g, "") + '"]');
    if (marca) marca.checked = true;
  } catch (e) {}
''')
    js_form = troca(js_form, "whatsapp: zap.value, area: AREA,", "whatsapp: zap.value, area: areaEscolhida(),")
    js_form = troca(js_form, 'if (dados.nome.length < 3) return mostrarErro("Escreva o seu nome completo.");',
                    'if (!dados.area) { var sel = document.getElementById("area"); if (sel) sel.scrollIntoView({ behavior: "smooth" }); return mostrarErro("Escolha a sua área, logo acima."); }\n      if (dados.nome.length < 3) return mostrarErro("Escreva o seu nome completo.");')
    principal = [x for x in scripts if "var EDGE" not in x]
    assert len(principal) == len(scripts) - 1, len(scripts)

    nicho = '<div id="nicho" class="vazio" data-area="prev">\n' + miolo(h) + "\n</div>"
    js_nicho = JS_NICHO.replace("__NOMES__", json.dumps({x: AREAS[x]["nome"] for x in ORDEM}, ensure_ascii=False))
    corpo = "\n\n".join([nav, HERO_VSL, secao_area, nicho, secao_teste, faq, final, rodape] + principal + [js_form, JS_VSL, js_nicho])
    pagina = cabeca + corpo + "\n</body>\n</html>\n" if "<body" in cabeca else cabeca + corpo + "\n</html>\n"
    ids = re.findall(r'\bid="([^"]+)"', pagina)
    assert len(ids) == len(set(ids)), sorted({x for x in ids if ids.count(x) > 1})
    for alvo in set(re.findall(r'href="#([^"]+)"', pagina)):
        assert alvo in ids, "âncora sem destino: " + alvo
    return pagina


SOBRAS = re.compile(r"previd|INSS|CNIS|aposent|benefício|auxílio|RMI|PPP|períci|segurado", re.I)


VAI_PARA_TESTE = """<!DOCTYPE html>
<html lang="pt-BR">
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<title>Teste a MaestrIA por 7 dias</title>
<script>
(function () {
  // Desde 25/11/2026 o teste tem uma página só: /teste/. Este endereço leva para ela com a área marcada,
  // mantendo a origem (?o=) de quem divulgou.
  var p = new URLSearchParams(location.search);
  if ("__AREA__") p.set("a", "__AREA__");
  var resto = p.toString();
  location.replace("/teste/" + (resto ? "?" + resto : ""));
})();
</script>
<noscript><meta http-equiv="refresh" content="0;url=/teste/__Q__"></noscript>
<p style="font-family:sans-serif;padding:24px">Abrindo o teste da MaestrIA. Se não abrir, <a href="/teste/__Q__">toque aqui</a>.</p>
</html>
"""


def main():
    h = todos(estrutura(BASE, "prev"))
    assert chr(8212) not in h
    (RAIZ / "teste" / "index.html").write_text(h, encoding="utf-8", newline="\n")
    print(f"página única: {len(h)} bytes -> teste/index.html")
    (RAIZ / "teste" / "nicho").mkdir(exist_ok=True)
    for a in ORDEM:
        h = estrutura(BASE, a)
        if a != "prev":
            h = conteudo(h, a)
        frag = miolo(h) + "\n" + "\n".join(scripts_da_pagina(h)) + "\n"
        assert chr(8212) not in frag
        (RAIZ / "teste" / "nicho" / f"{a}.html").write_text(frag, encoding="utf-8", newline="\n")
        print(f"teste/nicho/{a}.html: {len(frag)} bytes")
    for a in ORDEM + ["area"]:
        area = "" if a == "area" else a
        q = f"?a={area}" if area else ""
        destino = RAIZ / "teste" / a / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(VAI_PARA_TESTE.replace("__AREA__", area).replace("__Q__", q), encoding="utf-8", newline="\n")
        print(f"teste/{a}/ -> /teste/{q}")


if __name__ == "__main__":
    main()
