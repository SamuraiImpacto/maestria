# Monta /prev-marketing/index.html a partir das páginas /prev/ e /marketing/.
# Os blocos visuais (terminal, planilha, jurimetria, peneira, filtro da OAB,
# calendário, voz, site) vêm das duas páginas oficiais; aqui entra só o que é
# do combo: topo, comparação com o Claude sozinho, pacote, garantia e FAQ.
# Rodar de novo depois de mudar /prev/ ou /marketing/:  python prev-marketing/montar.py
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parent.parent
P = (RAIZ / 'prev/index.html').read_text(encoding='utf-8').split('\n')
M = (RAIZ / 'marketing/index.html').read_text(encoding='utf-8').split('\n')
CHECKOUT = 'https://pay.kiwify.com.br/urkdMlQ'


def trecho(linhas, ini, fim):
    """Linhas ini..fim (contagem a partir de 1, inclusive)."""
    return '\n'.join(linhas[ini - 1:fim])


def bloco(linhas, abre, fecha='</section>'):
    """Do primeiro `abre` até o `fecha` seguinte, inclusive."""
    i = next(n for n, l in enumerate(linhas) if l.startswith(abre))
    j = next(n for n in range(i, len(linhas)) if linhas[n].startswith(fecha))
    return '\n'.join(linhas[i:j + 1])


def entre(linhas, abre, fecha):
    i = next(n for n, l in enumerate(linhas) if l.strip().startswith(abre))
    j = next(n for n in range(i + 1, len(linhas)) if linhas[n].strip().startswith(fecha))
    return '\n'.join(linhas[i + 1:j])


cabeca = '\n'.join(l for l in P[:P.index('<style>')])
cabeca = re.sub(r'<title>.*?</title>', '<title>MaestrIA Previdenciário + Marketing: o que o Claude não faz sozinho</title>', cabeca)
cabeca = re.sub(r'<meta name="description" content="[^"]*">',
                '<meta name="description" content="Você já usa o Claude. A MaestrIA é o que ele não faz sozinho: cálculo do INSS com memória aberta, jurisprudência conferida no CNJ, petição no seu timbrado, intimações pela OAB, conteúdo com a sua voz, vídeo editado e site no ar. Previdenciário + Marketing por R$ 997.">', cabeca)
cabeca = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="MaestrIA Previdenciário + Marketing: o que o Claude não faz sozinho">', cabeca)
cabeca = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Você já usa o Claude. A MaestrIA é o que ele não faz sozinho, do cálculo do auxílio-acidente ao site do escritório. Os dois pacotes por R$ 997, com 12 meses de acesso.">', cabeca)
cabeca = cabeca.replace('https://maestria.samurailab.com.br/prev/', 'https://maestria.samurailab.com.br/prev-marketing/')

css_prev = entre(P, '<style>', '</style>')
# segundo bloco de estilo do Marketing (vitrines e calendário)
i2 = [n for n, l in enumerate(M) if l.strip() == '<style>'][1]
css_mkt = entre(M[i2:], '<style>', '</style>')

CSS_COMBO = r'''
  /* ===== combo Prev + Marketing ===== */
  .logo .sub{white-space:nowrap}
  .vs{margin:44px auto 0;max-width:1040px;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--panel);text-align:left}
  .vs-head,.vs-row{display:grid;grid-template-columns:1.05fr 1.45fr 1.75fr}
  .vs-head div{padding:15px 20px;font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--muted-2);background:var(--panel-2)}
  .vs-head div:last-child{color:var(--red-ink)}
  .vs-row{border-top:1px solid var(--line)}
  .vs-row>div{padding:17px 20px;font-size:15.5px;line-height:1.55}
  .vs-row .tema{font-weight:700;display:flex;gap:10px;align-items:flex-start}
  .vs-row .tema .ic{flex:0 0 auto}
  .vs-row .so{color:var(--muted)}
  .vs-row .so::before{content:"✕";color:var(--muted-2);font-weight:800;margin-right:8px}
  .vs-row .com{background:linear-gradient(90deg,rgba(239,39,39,.07),transparent 85%)}
  .vs-row .com::before{content:"✓";color:var(--green);font-weight:800;margin-right:8px}
  .vs-row .com b{color:var(--red-ink);font-weight:700}
  .vs-row .rot{display:none}
  .vs-pe{margin:22px auto 0;max-width:62ch;color:var(--muted-2);font-size:14.5px;text-align:center}
  .divisor{padding:40px 0 0}
  .divisor .wrap{text-align:center}
  .divisor .pilula{display:inline-flex;align-items:center;gap:10px;border:1px solid var(--line-strong);border-radius:999px;padding:9px 18px;font-weight:800;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--txt);background:var(--panel)}
  .divisor .pilula i{width:9px;height:9px;border-radius:50%;background:var(--red);box-shadow:0 0 0 4px var(--red-soft)}
  .divisor h2{margin-top:18px}
  .emb.combo{max-width:860px}
  .emb.combo .duas-listas{display:grid;grid-template-columns:1fr 1fr;gap:6px 26px;text-align:left}
  .emb.combo .duas-listas .h{margin-top:4px}
  .combo-soma{margin-top:10px;color:var(--muted);font-size:15px}
  .combo-soma s{color:var(--muted-2)}
  @media (max-width:760px){
    .vs-head{display:none}
    .vs-row{grid-template-columns:1fr}
    .vs-row>div{padding:5px 18px}
    .vs-row .tema{padding-top:18px;font-size:16.5px}
    .vs-row .com{padding-bottom:18px;background:none}
    .vs-row .so::before,.vs-row .com::before{content:none}
    .vs-row .rot{display:block;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted-2)}
    .vs-row .com .rot{color:var(--red-ink)}
    .emb.combo{max-width:860px}
  .emb.combo .duas-listas{grid-template-columns:1fr}
  }
'''

ICONE = lambda d: f'<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg></span>'
KI = lambda d: f'<svg class="ki" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
I_CALC = '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8"/><path d="M8 11h.01"/><path d="M12 11h.01"/><path d="M16 11h.01"/><path d="M8 15h.01"/><path d="M12 15h.01"/><path d="M16 15h.01"/>'
I_DOC = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h8"/>'
I_BALANCA = '<path d="M12 3v18"/><path d="M5 7h14"/><path d="m5 7-3 7a4 4 0 0 0 6 0Z"/><path d="m19 7-3 7a4 4 0 0 0 6 0Z"/>'
I_BARRA = '<path d="M3 3v18h18"/><path d="M7 16v-4"/><path d="M12 16V8"/><path d="M17 16v-7"/>'
I_SINO = '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'
I_GRADE = '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'
I_VIDEO = '<rect x="2" y="5" width="15" height="14" rx="2"/><path d="m17 10 5-3v10l-5-3Z"/>'
I_GLOBO = '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18"/><path d="M12 3a14 14 0 0 0 0 18"/>'
I_RAIO = '<path d="M13 2 3 14h9l-1 8 10-12h-9Z"/>'
I_ESTRELA = '<path d="m12 2 3 6.9 7.5 1-5.5 5.2 1.4 7.4L12 19l-6.4 3.5L7 15.1 1.5 9.9 9 8.9Z"/>'
I_DUVIDA = '<circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>'

COMPARA = [
    (I_CALC, 'Calcular o auxílio-acidente',
     'Faz a conta na conversa, sem índice oficial conferido. Você refaz para confiar.',
     'Lê a carta de concessão, calcula com <b>motor testado</b> e os reajustes oficiais do INSS e entrega o Excel com a memória aberta, mês a mês.'),
    (I_BALANCA, 'Citar jurisprudência',
     'Pode citar número de processo que não existe, com toda a segurança do mundo.',
     'Confere cada decisão <b>na base do CNJ e no site do tribunal</b>. O que não existe é descartado antes de chegar em você.'),
    (I_DOC, 'Escrever a petição',
     'Texto genérico, que você copia, ajusta e formata no Word.',
     'Lê os documentos do caso e escreve <b>no seu estilo e no seu timbrado</b>, a partir de 1 ou 2 modelos seus. Sai em Word.'),
    (I_BARRA, 'Escolher onde entrar com a ação',
     'Opinião geral, sem o número de nenhuma vara.',
     'Taxa de procedência por vara com o <b>dado oficial do CNJ</b>, antes de ajuizar.'),
    (I_SINO, 'Acompanhar prazos',
     'Não acessa as suas publicações.',
     'Busca as <b>intimações pela sua OAB</b> no Diário da Justiça todo dia e calcula o vencimento.'),
    (I_GRADE, 'Postar no Instagram',
     'Texto com cara de robô e sem arte. Você ainda abre o Canva e monta tudo.',
     'Carrossel e post <b>com a sua voz e a sua marca</b>, legenda e arte prontas, já passados pelo Provimento 205.'),
    (I_VIDEO, 'Editar o vídeo que você gravou',
     'Não edita vídeo.',
     'Tira as pausas, põe <b>legenda e gancho</b> e devolve o MP4 para você revisar.'),
    (I_GLOBO, 'Ter um site',
     'Te dá um código solto e você que se vire para colocar no ar.',
     'Constrói o site com blog e te guia até o ar, <b>no seu domínio, com hospedagem gratuita</b>.'),
]
linhas_cmp = '\n'.join(
    f'      <div class="vs-row" role="row"><div class="tema" role="cell"><span>{t}</span></div>'
    f'<div class="so" role="cell"><span class="rot">Claude sozinho</span>{s}</div>'
    f'<div class="com" role="cell"><span class="rot">Com MaestrIA</span>{c}</div></div>'
    for ic, t, s, c in COMPARA)

NAV = f'''<nav>
  <div class="wrap nav-in">
    <a class="logo" href="/" aria-label="MaestrIA Previdenciário + Marketing"><img class="sym" src="/img/logo-sym.png" alt=""><img class="word" src="/img/logo-word.png" alt="MaestrIA"><span class="sub">Prev + Marketing</span></a>
    <div class="nav-links">
      <a href="#diferenca">A diferença</a>
      <a href="#acoes">O que dá pra pedir</a>
      <a href="#peticao">Previdenciário</a>
      <a href="#conteudo">Marketing</a>
      <a href="#pacotes" class="btn btn-red btn-sm nav-cta">Quero os dois</a>
    </div>
  </div>
</nav>'''

HERO = '''<header class="hero">
  <div class="hero-art" id="heroArt" aria-hidden="true"><img src="/img/logo-sym.png" alt=""></div>
  <div class="wrap">
    <span class="eyebrow"><i></i>MaestrIA Previdenciário + Marketing &nbsp;•&nbsp; roda no seu computador</span>
    <h1 class="big">Você já usa o Claude. A MaestrIA é o que ele <span class="red">não sabe fazer sozinho</span>.</h1>
    <p class="hero-sub">O Claude é o cérebro. A MaestrIA é o escritório que ele passa a conhecer: o motor de cálculo do INSS, a conferência da jurisprudência na fonte, o seu timbrado, a sua marca e o passo a passo de cada tarefa. Você continua digitando <span class="cmd">/maestria</span> e pedindo em português. <b>Muda o que volta.</b></p>
    <div class="hero-cta">
      <a href="#pacotes" class="btn btn-red">Quero os dois por R$ 997</a>
      <a href="#diferenca" class="btn btn-ghost">Ver a diferença na prática</a>
    </div>
    <p class="hero-tiny">Previdenciário e Marketing juntos, com 12 meses de acesso. Único pré-requisito: uma assinatura do Claude.</p>

    <div class="term" id="term">
      <div class="term-bar">
        <span class="d r"></span><span class="d y"></span><span class="d g"></span>
        <span class="term-title">Claude Code: MaestrIA Previdenciário + Marketing</span>
      </div>
      <div class="term-body" id="termbody">
        <p class="tl t-cmd"><span class="p">&gt;</span>/maestria calcular auxílio-acidente</p>
        <p class="tl t-resp">Lendo a carta de concessão na pasta do cliente... RMI do auxílio-doença R$ 2.104,33.</p>
        <p class="tl t-resp">Valor atual, reajustado pelos índices oficiais do INSS: <span class="t-ok">R$ 1.243,80 ✓</span></p>
        <p class="tl t-ok">✓ AuxilioAcidente_Calculo.xlsx com a memória aberta, mês a mês</p>
        <p class="tl t-cmd"><span class="p">&gt;</span>/maestria carrossel sobre quem tem direito ao auxílio-acidente</p>
        <p class="tl t-resp">Puxando o seu tom de voz e a persona "trabalhador acidentado"...</p>
        <p class="tl t-resp">Filtro do Provimento 205 aplicado: sem promessa de resultado.</p>
        <p class="tl t-ok">✓ 8 lâminas com a sua marca e a legenda prontas para postar</p>
        <p class="tl t-dim">Valores ilustrativos. Índices validados em fonte oficial (gov.br).<span class="cursor" id="cur"></span></p>
      </div>
    </div>
  </div>
</header>'''

FAIXA = ['Nunca inventa jurisprudência', 'Dado do cliente no seu computador', 'Cálculo com memória aberta',
         'Intimações pela sua OAB', 'Conteúdo com a sua voz', 'Provimento 205 da OAB', 'Site no seu domínio', 'Licença no seu CPF']
MARQ = ('<div class="marq" aria-hidden="true">\n  <div class="marq-track">\n    '
        + ''.join(f'<span>{t}</span>' for t in FAIXA) + '\n    ' + ''.join(f'<span>{t}</span>' for t in FAIXA)
        + '\n  </div>\n</div>')

DIFERENCA = f'''<section id="diferenca">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_RAIO)}<span>Claude sozinho x Claude com MaestrIA</span></span>
    <h2 class="sec reveal">O mesmo pedido. <span class="red">Duas respostas diferentes</span>.</h2>
    <p class="lead reveal">O Claude sozinho conversa muito bem. Mas ele não conhece o seu escritório, não tem o motor de cálculo do INSS e não confere se a decisão que citou existe. E a cada conversa nova, começa do zero.</p>
    <div class="vs reveal" role="table" aria-label="Comparação entre o Claude sozinho e o Claude com a MaestrIA">
      <div class="vs-head" role="row"><div role="columnheader">Você pede</div><div role="columnheader">Claude sozinho</div><div role="columnheader">Claude com MaestrIA</div></div>
{linhas_cmp}
    </div>
    <p class="vs-pe reveal">É o mesmo Claude que você já assina. A MaestrIA se instala dentro dele: não é outro site, outro login nem outra tela.</p>
  </div>
</section>'''

# Ações: 4 do Previdenciário + 4 do Marketing, com os roteiros das duas páginas
ACOES_BOTOES = [('calculo', 'Calcular RMI e atrasados'), ('pericia', 'Preparar a perícia'),
                ('lead', 'Qualificar o caso de auxílio-acidente'), ('vara', 'Descobrir a melhor vara'),
                ('carrossel', 'Escrever o carrossel da semana'), ('calendario', 'Montar o calendário do mês'),
                ('site', 'Construir o site do escritório'), ('landing', 'Criar a página da campanha')]
acoes = bloco(P, '<section class="acoes"')
lista = '\n'.join(f'      <button class="acao{" on" if n == 0 else ""}" data-ac="{k}">{t}<i>›</i></button>'
                  for n, (k, t) in enumerate(ACOES_BOTOES))
acoes = re.sub(r'(<div class="acoes-lista reveal">\n).*?(\n    </div>)', lambda m: m.group(1) + lista + m.group(2), acoes, flags=re.S)
acoes = acoes.replace('Claude Code: MaestrIA Previdenciário', 'Claude Code: MaestrIA')

DIV_PREV = f'''<section class="divisor">
  <div class="wrap">
    <span class="pilula reveal"><i></i>Parte 1 · Previdenciário</span>
    <h2 class="sec reveal">O trabalho mecânico que vem <span class="red">antes da tese</span>.</h2>
  </div>
</section>'''
DIV_MKT = f'''<section class="divisor">
  <div class="wrap">
    <span class="pilula reveal"><i></i>Parte 2 · Marketing</span>
    <h2 class="sec reveal">O escritório aparecendo <span class="red">para quem precisa dele</span>.</h2>
  </div>
</section>'''

prev_rows = '\n\n'.join(bloco(P, f'<section id="{s}"') for s in ('peticao', 'calculo', 'jurimetria', 'juris'))
mkt_rows = '\n\n'.join(bloco(M, f'<section id="{s}"') for s in ('conteudo', 'calendario', 'compliance', 'voz', 'seu'))
# a primeira seção depois do divisor não precisa do respiro de cima
prev_rows = prev_rows.replace('<section id="peticao">', '<section id="peticao" style="padding-top:56px">', 1)
mkt_rows = mkt_rows.replace('<section id="conteudo">', '<section id="conteudo" style="padding-top:56px">', 1)
sigilo = bloco(P, '<section id="sigilo"').replace('style="padding-top:0"', '', 1)

# Custo: o gráfico do Marketing, com a barra do combo
i_graf = next(n for n, l in enumerate(M) if 'id="graf"' in l)
i_sec = max(n for n in range(i_graf) if M[n].startswith('<section'))
custo = bloco(M[i_sec:], '<section')
custo = custo.replace('<span class="gf-rot">MaestrIA Marketing<em>uma vez, 1 ano de atualizações</em></span>',
                      '<span class="gf-rot">MaestrIA Prev + Marketing<em>os dois pacotes, 1 ano de atualizações</em></span>')
custo = custo.replace('<span>o pacote inteiro: menos que um mês de social media</span>',
                      '<span>os dois pacotes: menos que um mês de social media</span>')
# O gráfico vem da página do Marketing, que mostra o preço dele sozinho: aqui vale o do combo
assert custo.count('R$ 297')==2, 'o gráfico do Marketing mudou de forma'
custo = custo.replace('R$ 297', 'R$ 997')
custo = re.sub(r'Compare com o pacote inteiro,[^<]*', 'Compare com os dois pacotes da MaestrIA juntos: R$ 997 por 12 meses, com o operacional do previdenciário de brinde.', custo)

instalacao = bloco(P, '<section id="instalacao"')
instalacao = instalacao.replace('Travou em qualquer passo? Pede ajuda de dentro da própria skill e a gente te destrava.',
                                'Travou em qualquer passo? Manda um print no grupo da comunidade e a gente te destrava.')
instalacao = instalacao.replace('<span class="tr-d">cálculo, CNIS ou recurso, pronto pra sua revisão</span>',
                                '<span class="tr-d">um cálculo, uma petição ou o carrossel da semana, pronto pra sua revisão</span>')
instalacao = instalacao.replace('Da compra ao primeiro cálculo', 'Da compra ao primeiro resultado')

# Pacote: mesma moldura da página do Prev, com as duas listas
li = lambda b, t: f'          <li><span class="ck">✓</span><span><b>{b}:</b> {t}</span></li>'
L_PREV = [('Cálculo previdenciário completo', 'RMI, auxílio-acidente, atrasados e tempo especial, com memória aberta'),
          ('Auditor de CNIS', 'vínculo faltante e contribuição não computada, apontados em minutos'),
          ('Perícia de ponta a ponta', 'quesitos, impugnação de PPP e de laudo e o cliente preparado'),
          ('Qualificador de auxílio-acidente', 'acidente, sequela e qualidade de segurado, com o veredito na hora'),
          ('Petições no seu timbrado', 'gerador de documentos e revisor treinado nos seus critérios'),
          ('Jurisprudência conferida', 'cada decisão checada no CNJ e no site do tribunal'),
          ('Jurimetria oficial do CNJ', 'procedência e acordo por vara, antes de ajuizar'),
          ('Intimações pela sua OAB', 'publicações do dia com o vencimento calculado')]
L_MKT = [('Conteúdo com a sua voz', 'reels, carrosséis, estáticos e artigos calibrados nas suas personas'),
         ('Arte pronta', 'imagens com a sua marca ou o design direto na sua conta do Canva'),
         ('Edição de vídeo', 'pausas fora, legenda e gancho no vídeo que você gravou'),
         ('Calendário editorial', 'o mês inteiro de pauta da sua área em minutos'),
         ('Site do escritório no ar', 'com blog, no seu domínio, hospedado de graça'),
         ('Páginas de campanha', 'prontas para receber o anúncio do seu gestor de tráfego, com Pixel e WhatsApp'),
         ('Google Meu Negócio', 'da criação à rotina de quem procura advogado perto de casa'),
         ('Compliance OAB automático', 'tudo filtrado pelo Provimento 205 antes de sair')]
vitrines = re.search(r'    <div class="vitrines reveal">.*?\n    </div>\n', '\n'.join(M), re.S).group(0)
prereq = re.search(r'    <div class="cardy reveal" style="max-width:760px;margin:24px auto 0;text-align:center">\n      <h4 style="margin-bottom:8px">Único pré-requisito.*?\n    </div>\n', '\n'.join(P), re.S).group(0)

PACOTE = f'''<section id="pacotes" style="padding-top:20px">
  <div class="wrap">
    <div class="price-head reveal">
      <span class="kicker">{KI(I_ESTRELA)}<span>Preço e o que entra</span></span>
      <h2 class="sec">Os dois pacotes por <span class="red">R$ 997</span>, com 12 meses de acesso.</h2>
      <p class="lead">Previdenciário e Marketing completos, com todas as atualizações do período e licença no seu CPF em até 3 computadores.</p>
    </div>

    <div class="emb combo reveal">
      <span class="emb-tag">Os dois pacotes juntos</span>
      <div class="emb-name">MaestrIA Previdenciário + Marketing</div>
      <p class="emb-sub">Do cálculo do caso ao cliente novo chegando pelo Instagram, com a sua voz e citando fonte oficial.</p>
      <div class="emb-price">
        <span class="now"><span class="cur">R$</span><span class="val">997</span><span class="per">12 meses de acesso</span></span>
      </div>
      <p class="combo-soma">Uma compra, uma instalação, os dois pacotes. R$ 997 à vista ou 12x de R$ 103,11 no cartão.</p>
      <a href="{CHECKOUT}?src=lp-prev-marketing" class="btn btn-red" data-pacote="prev-marketing">Quero os dois por R$ 997</a>
      <div class="seals">
        <span><span class="s-ck">✓</span> Compra segura</span>
        <span><span class="s-ck">✓</span> 7 dias de garantia</span>
        <span><span class="s-ck">✓</span> Licença no seu CPF</span>
      </div>
      <div class="incl">
        <div class="duas-listas">
          <div><div class="h">Previdenciário</div><ul>
{chr(10).join(li(b, t) for b, t in L_PREV)}
          </ul></div>
          <div><div class="h">Marketing</div><ul>
{chr(10).join(li(b, t) for b, t in L_MKT)}
          </ul></div>
        </div>
      </div>
    </div>

    <p class="pacotes-pe">O pacote inclui <b>12 meses de acesso</b> com todas as atualizações do período e o <b>grupo da comunidade</b>, onde as dúvidas de uso são resolvidas.</p>

    <p class="pacotes-pe" data-aviso="trafego"><b>O anúncio pago continua com quem opera tráfego todo dia.</b> A MaestrIA entrega a página, o conteúdo e a pesquisa de praça que o seu gestor de tráfego precisa para subir a campanha. Ainda não tem um? A <b>Impacto Marketing Jurídico</b> opera o tráfego de escritórios de advocacia.</p>
{vitrines}
{prereq}  </div>
</section>'''

GARANTIA = '''<section style="padding-top:0">
  <div class="wrap">
    <div class="gar reveal">
      <div class="selo"><span><b>7</b><span>dias</span></span></div>
      <div class="gar-tx">
        <h3>Garantia incondicional de 7 dias</h3>
        <p>Instale, rode um caso real do INSS e gere um conteúdo do seu escritório. Se não fizer sentido pra você, devolvemos o valor integral, direto na plataforma de pagamento. Sem perguntas.</p>
      </div>
    </div>
  </div>
</section>'''

FAQS = [
    ('Eu já uso o Claude. Por que preciso da MaestrIA?',
     'Porque o Claude sozinho não tem o motor de cálculo do INSS, não confere jurisprudência na base do CNJ, não conhece o seu timbrado nem a sua marca, não busca as suas intimações e não edita vídeo. A MaestrIA dá isso a ele. Você continua usando o mesmo Claude, só que ele passa a trabalhar como alguém do seu escritório.'),
    ('Substitui a agência de tráfego?',
     'Não. A MaestrIA produz o site, a landing, o conteúdo e a pesquisa de praça. O anúncio pago continua com quem opera tráfego todo dia: subir a campanha, acompanhar a verba e ajustar o que não converte. Ela entrega o material que o seu gestor de tráfego precisa. Ainda não tem um? A Impacto Marketing Jurídico opera o tráfego de escritórios de advocacia.'),
    ('Inventa acórdão como o ChatGPT?',
     'Não. Toda decisão passa pela base do CNJ e pelo site do tribunal, e leis, súmulas e temas são conferidos em fonte oficial. Quando não dá pra confirmar, ela avisa em vez de inventar.'),
    ('Os dados dos meus clientes ficam seguros?',
     'Sim. CPF, laudo, CNIS e processo ficam em pastas suas, no seu computador ou no seu Google Drive. Nada vai pra servidor nosso.'),
    ('A MaestrIA conversa com o meu cliente?',
     'Não. Ela trabalha para você: você cola o relato do cliente ou os documentos e ela devolve o material pronto para a sua revisão.'),
    ('Preciso saber programar? Funciona no Mac?',
     'Não precisa programar, e funciona no Windows e no Mac. Você arrasta o arquivo pra conversa do Claude e pede pra instalar. Tem <a href="/instalacao.html" style="color:var(--red-ink)">guia passo a passo</a> e, se travar, o grupo da comunidade te ajuda.'),
    ('Por que preciso de assinatura do Claude?',
     'O Claude é a inteligência que faz o trabalho pesado, e a MaestrIA é a camada jurídica e de marketing que roda em cima dele. A assinatura é contratada direto no claude.ai e é o único custo fora da MaestrIA.'),
]
FAQ = (f'''<section id="faq" style="padding-top:0">
  <div class="wrap">
    <span class="kicker reveal">{KI(I_DUVIDA)}<span>FAQ</span></span>
    <h2 class="sec reveal" style="margin-bottom:32px">O que mais perguntam.</h2>
''' + '\n'.join(f'    <details class="faq reveal"><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in FAQS)
       + '\n  </div>\n</section>')

FINAL = '''<section class="final">
  <div class="wrap">
    <h2 class="reveal">O Claude você já tem. <span class="red">Falta ele conhecer o seu escritório</span>.</h2>
    <p class="reveal">Instala em meia hora e, no mesmo dia, roda o primeiro cálculo e o primeiro carrossel no padrão do seu escritório.</p>
    <a href="#pacotes" class="btn btn-red btn-lg reveal">Quero os dois por R$ 997</a>
    <p class="cta-meta reveal"><span>Setup em 30 minutos</span><span>Sigilo local</span><span>Citação validada em fonte oficial</span><span>Garantia de 7 dias</span></p>
  </div>
</section>'''

rodape = bloco(P, '<footer>', '</footer>')
rodape = rodape.replace('<a href="#pacotes">O pacote</a><a href="#peticao">O que ela faz</a><a href="#faq">FAQ</a><a href="/">Todas as áreas</a>',
                        '<a href="#pacotes">O pacote</a><a href="/prev/">Só o Previdenciário</a><a href="/marketing/">Só o Marketing</a><a href="/">Todas as áreas</a>')

# Script principal do Prev, com os roteiros do Marketing somados
i_scr = max(n for n, l in enumerate(P) if l.startswith('<script>'))
script = '\n'.join(P[i_scr:P.index('</script>', i_scr) + 1])
rot_mkt = re.search(r'var ROTEIROS = \{\n(.*?)\n    \};', '\n'.join(M), re.S).group(1)
script = re.sub(r'(var ROTEIROS = \{\n.*?)(\n    \};)', lambda m: m.group(1) + ',\n' + rot_mkt + m.group(2), script, count=1, flags=re.S)

# Se a pessoa já clicou num botão antes da seção aparecer, não passa por cima do roteiro dela
script = script.replace("if(e.isIntersecting){ rodarRoteiro('calculo'); oAc.disconnect(); }",
                        "if(e.isIntersecting){ if(!acToken) rodarRoteiro('calculo'); oAc.disconnect(); }")
assert 'if(!acToken)' in script

html = '\n'.join([
    cabeca, '<style>', css_prev, css_mkt, CSS_COMBO, '</style>', '',
    NAV, '', HERO, '', MARQ, '', DIFERENCA, '', acoes, '',
    DIV_PREV, '', prev_rows, '', DIV_MKT, '', mkt_rows, '', sigilo, '', custo, '', instalacao, '',
    PACOTE, '', GARANTIA, '', FAQ, '', FINAL, '', rodape, '', script, '</html>', ''])

# Travas: nada do checkout avulso, nada de promoção vencida, nada de travessão
for proibido in ('q5QEizf', 'Ln4ErJJ', 'so-promo', '—', 'Quero o Previdenciário', 'Quero o Marketing'):
    assert proibido not in html.split('</style>', 1)[1], proibido
ids = re.findall(r'\bid="([^"]+)"', html)
assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})

(RAIZ / 'prev-marketing/index.html').write_text(html, encoding='utf-8')
print('ok', len(html), 'bytes')
