"""Gera a página do teste grátis de cada área a partir de uma base só.

Uso:  python _ferramentas/gerar_teste_areas.py

Entradas:
  _ferramentas/teste-base.html  a página do teste de previdenciário, como foi aprovada
  _ferramentas/areas.json       título, frase e ferramentas de cada área
  <area>/index.html             a página de venda de cada pacote, de onde saem as demonstrações

Saídas:
  teste/index.html              previdenciário (endereço único divulgado)
  teste/<area>/index.html       as outras sete áreas
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
    return "/teste/" if a == "prev" else f"/teste/{a}/"


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
  var areas = { trab: 1, familia: 1, consumidor: 1, bancario: 1, criminal: 1, imobiliario: 1, empresarial: 1 };
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

SOBRAS = re.compile(r"previd|INSS|CNIS|aposent|benefício|auxílio|RMI|PPP|períci|segurado", re.I)


def main():
    for a in ORDEM:
        h = estrutura(BASE, a)
        if a != "prev":
            h = conteudo(h, a)
        assert chr(8212) not in h
        destino = RAIZ / "teste" / ("index.html" if a == "prev" else f"{a}/index.html")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(h, encoding="utf-8", newline="\n")
        sobras = []
        if a != "prev":
            corpo = re.sub(r"<style>.*?</style>", "", h, flags=re.S)
            corpo = re.sub(r'<div class="areas-barra".*?</div>', "", corpo, flags=re.S)
            for linha in corpo.split("\n"):
                for m in SOBRAS.finditer(linha):
                    sobras.append(re.sub(r"<[^>]+>", " ", linha)[max(0, m.start() - 200):][:160].strip() if len(linha) < 400 else re.sub(r"<[^>]+>", " ", linha[max(0, m.start() - 60):m.start() + 90]).strip())
        print(f"{a}: {len(h)} bytes -> {destino.relative_to(RAIZ)} | sobras de previdenciário: {len(sobras)}")
        if "--sobras" in sys.argv:
            for s in sorted(set(sobras)):
                print("    ·", s)
    (RAIZ / "teste" / "area" / "index.html").write_text(REDIRECIONA, encoding="utf-8", newline="\n")
    print("teste/area/index.html: redirecionamento")


if __name__ == "__main__":
    main()
