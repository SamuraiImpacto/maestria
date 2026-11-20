# Monta /teste/index.html: a página do teste grátis de 7 dias (Previdenciário + Marketing).
# Aproveita os blocos que o /prev-marketing/montar.py já monta a partir de /prev/ e /marketing/
# (comparação com o Claude sozinho, demonstrações, seções de cada ferramenta, sigilo, instalação)
# e troca o que é de venda (preço, compra, garantia) pelo que é do teste (formulário, o que
# precisa, como são os 7 dias, o que acontece no fim).
# Rodar de novo depois de mudar /prev/, /marketing/ ou o montar do combo:  python teste/montar.py
from pathlib import Path
import re

RAIZ = Path(__file__).resolve().parent.parent
fonte = (RAIZ / 'prev-marketing/montar.py').read_text(encoding='utf-8')
# Só a parte que monta os blocos; a que grava a página do combo fica de fora.
corte = fonte.index("html = '\\n'.join([")
ns = {'__file__': str(RAIZ / 'prev-marketing/montar.py')}
exec(compile(fonte[:corte], 'prev-marketing/montar.py', 'exec'), ns)
g = lambda nome: ns[nome]
KI, I_RAIO, I_ESTRELA, I_DUVIDA = g('KI'), g('I_RAIO'), g('I_ESTRELA'), g('I_DUVIDA')
I_RELOGIO = '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
I_CHECK = '<path d="M20 6 9 17l-5-5"/>'
I_PC = '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/><path d="M12 16v4"/>'

cabeca = g('cabeca')
cabeca = re.sub(r'<title>.*?</title>', '<title>Teste a MaestrIA por 7 dias: Previdenciário + Marketing</title>', cabeca)
cabeca = re.sub(r'<meta name="description" content="[^"]*">',
                '<meta name="description" content="Teste por 7 dias, sem cartão, a MaestrIA Previdenciário + Marketing: cálculo do INSS com memória aberta, petição no seu timbrado, jurisprudência conferida, conteúdo com a sua voz. Roda no seu computador, dentro do Claude.">', cabeca)
cabeca = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Teste a MaestrIA por 7 dias, sem cartão">', cabeca)
cabeca = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="Previdenciário e Marketing completos, no seu computador, por 7 dias. Você só decide depois de usar.">', cabeca)
cabeca = cabeca.replace('https://maestria.samurailab.com.br/prev-marketing/', 'https://maestria.samurailab.com.br/teste/')
if '<meta name="robots"' not in cabeca:
    cabeca = cabeca.replace('<title>', '<meta name="robots" content="noindex">\n<title>', 1)

CSS_TESTE = r'''
  /* ===== teste grátis de 7 dias ===== */
  /* A manchete do teste é menor que a das páginas de venda: a primeira dobra precisa mostrar o texto e o botão. */
  header.hero{padding-top:48px}
  header.hero h1.big{font-size:clamp(2.1rem,4.4vw,3.5rem);line-height:1.08;max-width:20ch;margin-top:18px}
  header.hero .hero-sub{margin-top:16px}
  header.hero .hero-cta{margin-top:22px}
  @media (min-width:701px){.hero-fatos{justify-content:center}}
  .hero-fatos{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:18px;font-size:14.5px;color:var(--muted)}
  .hero-fatos span{display:inline-flex;align-items:center;gap:8px}
  .hero-fatos b{color:var(--green);font-weight:800}
  .precisa{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:38px;text-align:left}
  .precisa .cardy{padding:24px}
  .precisa .num{display:inline-flex;width:38px;height:38px;border-radius:50%;background:var(--red-soft);color:var(--red-ink);align-items:center;justify-content:center;margin-bottom:14px}
  .precisa .num svg{width:20px;height:20px}
  .precisa h3{font-size:17px}
  .precisa p{font-size:15px}
  .precisa a{color:var(--red-ink)}
  .dias{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:38px;text-align:left}
  .dia{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px}
  .dia .q{font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--red-ink)}
  .dia b{display:block;margin:8px 0 6px;font-size:16.5px}
  .dia span{color:var(--muted);font-size:14.5px;line-height:1.6}
  .dia.fim{border-color:rgba(70,209,127,.35);background:linear-gradient(180deg,rgba(70,209,127,.07),transparent)}
  .dia.fim .q{color:var(--green)}
  .teste-grade{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:start;margin-top:40px;text-align:left}
  .teste-form{background:linear-gradient(180deg,#17171b,#101013);border:1px solid var(--line-strong);border-radius:20px;padding:28px 26px;position:sticky;top:20px}
  .teste-form h3{font-size:1.3rem;margin-bottom:4px}
  .teste-form .sub{color:var(--muted);font-size:15px;margin-bottom:18px}
  .teste-form form{display:flex;flex-direction:column;gap:15px}
  .tf-campo{display:flex;flex-direction:column;gap:6px}
  .tf-campo label{font-weight:700;font-size:15px}
  .tf-campo .dica{display:block;color:var(--muted-2);font-size:13px;font-weight:400;margin-top:2px}
  .teste-form input[type=text],.teste-form input[type=tel],.teste-form input[type=email]{
    width:100%;background:var(--bg);color:var(--txt);border:1px solid var(--line-strong);border-radius:12px;padding:14px;font:inherit;font-size:16px}
  .teste-form input:focus{outline:2px solid var(--red-ink);outline-offset:1px;border-color:transparent}
  .tf-isca{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
  .tf-erro{color:var(--red-ink);font-weight:600}
  .tf-legal{color:var(--muted-2);font-size:13px;line-height:1.5}
  .teste-form .btn{width:100%}
  .teste-form .btn:disabled{opacity:.6;cursor:wait}
  .tf-gira{display:none;width:16px;height:16px;border:2px solid rgba(255,255,255,.4);border-top-color:#fff;border-radius:50%;animation:tfgira .8s linear infinite}
  .carregando .tf-gira{display:inline-block}
  @keyframes tfgira{to{transform:rotate(360deg)}}
  .tf-selo{display:inline-flex;width:46px;height:46px;border-radius:50%;background:rgba(70,209,127,.15);color:var(--green);font-size:24px;font-weight:800;align-items:center;justify-content:center;margin-bottom:14px}
  .tf-oculto{display:none !important}
  .teste-inclui .h{font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--red-ink);margin:0 0 10px}
  .teste-inclui .h+ul{margin-bottom:24px}
  .teste-inclui ul{list-style:none;display:flex;flex-direction:column;gap:9px}
  .teste-inclui li{display:flex;gap:10px;font-size:15px;line-height:1.5;color:var(--muted)}
  .teste-inclui li b{color:var(--txt)}
  .teste-inclui .ck{color:var(--green);font-weight:800;flex:0 0 auto}
  .cta-meio{padding:8px 0 0;text-align:center}
  .cta-meio p{color:var(--muted-2);font-size:14px;margin-top:12px}
  @media (prefers-reduced-motion:reduce){.tf-gira{animation:none}}
  @media (max-width:900px){
    .precisa,.dias{grid-template-columns:1fr 1fr}
    .teste-grade{grid-template-columns:1fr}
    .teste-form{position:static}
  }
  @media (max-width:560px){.precisa,.dias{grid-template-columns:1fr}}
'''

NAV = '''<nav>
  <div class="wrap nav-in">
    <a class="logo" href="/" aria-label="MaestrIA: teste grátis"><img class="sym" src="/img/logo-sym.png" alt=""><img class="word" src="/img/logo-word.png" alt="MaestrIA"><span class="sub">Teste grátis</span></a>
    <div class="nav-links">
      <a href="#diferenca">O que ela faz</a>
      <a href="#acoes">Veja funcionando</a>
      <a href="#precisa">O que você precisa</a>
      <a href="#dias">Como são os 7 dias</a>
      <a href="#teste" class="btn btn-red btn-sm nav-cta">Testar 7 dias grátis</a>
    </div>
  </div>
</nav>'''

HERO = '''<header class="hero">
  <div class="hero-art" id="heroArt" aria-hidden="true"><img src="/img/logo-sym.png" alt=""></div>
  <div class="wrap">
    <span class="eyebrow"><i></i>Teste grátis de 7 dias &nbsp;•&nbsp; Previdenciário + Marketing</span>
    <h1 class="big">Teste a MaestrIA por 7&nbsp;dias, <span class="red">sem pagar nada</span>.</h1>
    <p class="hero-sub">A MaestrIA é uma inteligência artificial que se instala no seu computador e faz o trabalho operacional do escritório previdenciário: lê os documentos do cliente, calcula, escreve a petição no seu timbrado, confere a jurisprudência e ainda produz o conteúdo do seu Instagram com a sua voz. Você pede em português comum, como numa conversa. <b>Quem revisa e decide é você.</b></p>
    <div class="hero-cta">
      <a href="#teste" class="btn btn-red">Quero testar por 7 dias</a>
      <a href="#diferenca" class="btn btn-ghost">Ver o que ela faz</a>
    </div>
    <div class="hero-fatos"><span><b>✓</b> Sem cartão</span><span><b>✓</b> Sem cobrança automática</span><span><b>✓</b> Os dois pacotes completos</span><span><b>✓</b> Com os seus casos</span></div>

    <div class="term" id="term">
      <div class="term-bar">
        <span class="d r"></span><span class="d y"></span><span class="d g"></span>
        <span class="term-title">Você escreve o pedido. A MaestrIA devolve o trabalho pronto.</span>
      </div>
      <div class="term-body" id="termbody">
        <p class="tl t-cmd"><span class="p">&gt;</span>quero dar entrada no auxílio-acidente desse cliente, faz tudo até o protocolo</p>
        <p class="tl t-resp">Lendo a pasta do cliente: carta de concessão, laudo, extrato de contribuições...</p>
        <p class="tl t-resp">Linha do tempo montada. Faltam 2 documentos, já anotados para você pedir.</p>
        <p class="tl t-ok">✓ Cálculo com a memória aberta, mês a mês, em Excel</p>
        <p class="tl t-ok">✓ Petição no seu timbrado, quesitos, procuração e contrato, em Word</p>
        <p class="tl t-cmd"><span class="p">&gt;</span>cria um carrossel sobre quem tem direito ao auxílio-acidente</p>
        <p class="tl t-resp">Usando o seu tom de voz. Filtro das regras da OAB aplicado: sem promessa de resultado.</p>
        <p class="tl t-ok">✓ 8 lâminas com a sua marca e a legenda prontas para você revisar</p>
        <p class="tl t-dim">Exemplo ilustrativo. O advogado revisa tudo antes de usar.<span class="cursor" id="cur"></span></p>
      </div>
    </div>
  </div>
</header>'''

DIFERENCA = g('DIFERENCA')
DIFERENCA = DIFERENCA.replace('O mesmo pedido. <span class="red">Duas respostas diferentes</span>.',
                              'O que a MaestrIA faz que a <span class="red">IA comum não faz</span>.')
DIFERENCA = DIFERENCA.replace('O Claude sozinho conversa muito bem. Mas ele não conhece o seu escritório, não tem o motor de cálculo do INSS e não confere se a decisão que citou existe. E a cada conversa nova, começa do zero.',
                              'A MaestrIA funciona dentro do Claude, um aplicativo de inteligência artificial. Sozinho, o Claude conversa muito bem, mas não conhece o seu escritório, não tem o motor de cálculo do INSS e não confere se a decisão que citou existe. Veja a diferença, pedido por pedido.')
DIFERENCA = DIFERENCA.replace('É o mesmo Claude que você já assina. A MaestrIA se instala dentro dele: não é outro site, outro login nem outra tela.',
                              'A MaestrIA se instala dentro do Claude: não é outro site, outro login nem outra tela para aprender.')
assert 'IA comum não faz' in DIFERENCA and 'pedido por pedido' in DIFERENCA

CTA_MEIO = '''<section class="cta-meio">
  <div class="wrap">
    <a href="#teste" class="btn btn-red btn-lg reveal">Quero testar tudo isso por 7 dias</a>
    <p class="reveal">Sem cartão. Você libera o teste em um minuto.</p>
  </div>
</section>'''

PRECISA = f'''<section id="precisa">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_CHECK)}<span>Antes de começar</span></span>
    <h2 class="sec reveal">O que você precisa ter para <span class="red">fazer o teste</span>.</h2>
    <p class="lead reveal">São só três coisas. Se faltar alguma, a área de membros mostra como resolver, com a imagem de cada tela.</p>
    <div class="precisa reveal">
      <div class="cardy">
        <span class="num">{KI(I_PC).replace('class="ki"', '')}</span>
        <h3>1. Um computador</h3>
        <p>Windows ou Mac. A MaestrIA trabalha com os arquivos do seu computador, por isso <b>não funciona no celular</b>. Não precisa ser uma máquina potente.</p>
      </div>
      <div class="cardy red-edge">
        <span class="num">{KI(I_ESTRELA).replace('class="ki"', '')}</span>
        <h3>2. O aplicativo Claude, com assinatura</h3>
        <p>O Claude é o aplicativo de inteligência artificial onde a MaestrIA se instala. Ele tem uma <b>assinatura própria</b>, contratada direto em <a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a>. É o único custo durante o teste, e você continua com ele mesmo se não ficar com a MaestrIA.</p>
      </div>
      <div class="cardy">
        <span class="num">{KI(I_RELOGIO).replace('class="ki"', '')}</span>
        <h3>3. Meia hora para instalar</h3>
        <p>Uma vez só. Você baixa um arquivo, entrega ao Claude e escreve "instala pra mim". <b>Não precisa saber programar.</b> Travou? Manda um print no grupo e a gente resolve.</p>
      </div>
    </div>
  </div>
</section>'''

DIAS = f'''<section id="dias" style="padding-top:0">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_RELOGIO)}<span>Os 7 dias</span></span>
    <h2 class="sec reveal">Como é o teste, <span class="red">do primeiro ao último dia</span>.</h2>
    <div class="dias reveal">
      <div class="dia"><span class="q">Hoje</span><b>Você libera o teste</b><span>Preenche o formulário desta página. O acesso sai na hora e também vai para o seu e-mail.</span></div>
      <div class="dia"><span class="q">Dia 1</span><b>Instala e faz o primeiro pedido</b><span>A área de membros guia cada passo. No mesmo dia você roda um caso seu ou cria um conteúdo.</span></div>
      <div class="dia"><span class="q">Dias 2 a 7</span><b>Usa à vontade</b><span>Cálculo, petição, quesitos, carrossel, roteiro de vídeo. Tudo liberado, em um computador, com os seus casos.</span></div>
      <div class="dia fim"><span class="q">Dia 8</span><b>Você decide</b><span>O teste pausa sozinho. O que você fez continua na sua pasta. Para seguir, é só comprar a licença: volta a funcionar sem instalar nada de novo.</span></div>
    </div>
  </div>
</section>'''

li = lambda b, t: f'            <li><span class="ck">✓</span><span><b>{b}:</b> {t}</span></li>'
TESTE = f'''<section id="teste">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_ESTRELA)}<span>Liberar o teste</span></span>
    <h2 class="sec reveal">Os dois pacotes completos, <span class="red">por 7 dias, sem pagar nada</span>.</h2>
    <p class="lead reveal">Não é uma versão reduzida nem uma demonstração com caso inventado. É a ferramenta inteira, no seu computador.</p>
    <div class="teste-grade">
      <div class="teste-form reveal" id="cartao">
        <div id="tela-form">
          <h3>Liberar meu teste de 7 dias</h3>
          <p class="sub">Leva um minuto. O acesso chega na hora.</p>
          <form id="f" novalidate>
            <div class="tf-campo"><label for="nome">Nome completo</label><input type="text" id="nome" name="nome" autocomplete="name" maxlength="120" required></div>
            <div class="tf-campo"><label for="email">E-mail</label><input type="email" id="email" name="email" autocomplete="email" maxlength="160" required></div>
            <div class="tf-campo"><label for="whatsapp">WhatsApp com DDD</label><input type="tel" id="whatsapp" name="whatsapp" autocomplete="tel" inputmode="tel" placeholder="(11) 99999-9999" maxlength="20" required></div>
            <div class="tf-campo"><label for="cpf">CPF<span class="dica">É a chave da sua área de membros, e garante um teste por pessoa.</span></label><input type="text" id="cpf" name="cpf" inputmode="numeric" placeholder="000.000.000-00" maxlength="14" required></div>
            <div class="tf-isca" aria-hidden="true"><label>Site <input type="text" name="site" id="site" tabindex="-1" autocomplete="off"></label></div>
            <p class="tf-erro tf-oculto" id="erro" role="alert"></p>
            <button type="submit" class="btn btn-red btn-lg" id="enviar"><span class="tf-gira"></span><span id="enviar-txt">Quero testar por 7 dias</span></button>
            <p class="tf-legal">Usamos os seus dados só para liberar o teste e falar com você sobre a MaestrIA. Sem cartão e sem cobrança automática.</p>
          </form>
        </div>
        <div id="tela-ok" class="tf-oculto">
          <span class="tf-selo">✓</span>
          <h3 id="ok-titulo">Teste liberado!</h3>
          <p class="sub" id="ok-texto"></p>
          <a class="btn btn-red btn-lg" id="ok-btn" href="/membros/">Instalar agora, passo a passo</a>
          <p class="tf-legal" style="margin-top:14px">Também mandamos o acesso para o seu e-mail. Confira o spam se não achar.</p>
        </div>
      </div>
      <div class="teste-inclui reveal">
        <div class="h">Previdenciário</div>
        <ul>
{chr(10).join(li(b, t) for b, t in g('L_PREV'))}
        </ul>
        <div class="h">Marketing</div>
        <ul>
{chr(10).join(li(b, t) for b, t in g('L_MKT'))}
        </ul>
      </div>
    </div>
  </div>
</section>'''

instalacao = g('instalacao')
instalacao = instalacao.replace('Da compra ao primeiro resultado', 'Do cadastro ao primeiro resultado')
instalacao = instalacao.replace('<b>Compra e recebe no email</b>', '<b>Libera o teste nesta página</b>')
instalacao = instalacao.replace('<span class="tr-d">código de ativação e link do pacote</span>', '<span class="tr-d">o acesso sai na hora e vai para o seu e-mail</span>')
assert 'Do cadastro ao primeiro resultado' in instalacao and 'Libera o teste nesta página' in instalacao

FAQS = [
    ('Precisa de cartão? Vou ser cobrado no fim?',
     'Não. Você não informa cartão e não existe cobrança automática. No fim dos 7 dias o teste pausa, e você só paga se decidir comprar.'),
    ('O que é o Claude, e por que preciso dele?',
     'O Claude é um aplicativo de inteligência artificial, da empresa Anthropic. Ele é a inteligência que faz o trabalho pesado, e a MaestrIA é a camada jurídica e de marketing que se instala dentro dele. A assinatura do Claude é contratada direto em claude.ai e é o único custo durante o teste.'),
    ('O que acontece depois dos 7 dias?',
     'As ferramentas pausam no seu computador. Nada do que você fez é apagado: petições, cálculos e arquivos continuam na sua pasta. Para seguir usando, é só comprar a licença com o mesmo e-mail do teste. Ela volta a funcionar sem instalar nada de novo.'),
    ('Posso usar com casos reais?',
     'Pode. É a ferramenta completa. Os arquivos ficam em pastas suas, no seu computador. A inteligência artificial é a do Claude e segue as regras da sua conta lá.'),
    ('Não entendo nada de tecnologia. Consigo?',
     'Consegue. A instalação é guiada, com a imagem de cada tela, e o suporte é no grupo da comunidade: você manda um print e a gente diz o que fazer. No uso, você escreve o pedido em português comum.'),
    ('Inventa acórdão como o ChatGPT?',
     'Não. Toda decisão passa pela base do CNJ e pelo site do tribunal, e leis, súmulas e temas são conferidos em fonte oficial. Quando não dá para confirmar, ela avisa em vez de inventar.'),
    ('Em quantos computadores posso testar?',
     'O teste vale para um computador. A licença comprada vale para até 3.'),
    ('A MaestrIA substitui o advogado?',
     'Não. Ela faz o trabalho operacional e mostra os caminhos. Quem revisa, decide e assina é você.'),
]
FAQ = (f'''<section id="faq" style="padding-top:0">
  <div class="wrap">
    <span class="kicker reveal">{KI(I_DUVIDA)}<span>Perguntas comuns</span></span>
    <h2 class="sec reveal" style="margin-bottom:32px">O que mais perguntam sobre o teste.</h2>
''' + '\n'.join(f'    <details class="faq reveal"><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in FAQS)
       + '\n  </div>\n</section>')

FINAL = '''<section class="final">
  <div class="wrap">
    <h2 class="reveal">Sete dias para ver funcionando <span class="red">no seu escritório</span>.</h2>
    <p class="reveal">Instala em meia hora e, no mesmo dia, roda o primeiro cálculo e o primeiro carrossel no padrão do seu escritório.</p>
    <a href="#teste" class="btn btn-red btn-lg reveal">Quero testar por 7 dias</a>
    <p class="cta-meta reveal"><span>Sem cartão</span><span>Os dois pacotes completos</span><span>No seu computador</span><span>Você decide no fim</span></p>
  </div>
</section>'''

rodape = g('rodape')
rodape = rodape.replace('<a href="#pacotes">O pacote</a>', '<a href="#teste">Testar 7 dias</a>')

SCRIPT_FORM = r'''<script>
(function () {
  var EDGE = "https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1/teste-gratis";
  var f = document.getElementById("f");
  if (!f) return;
  var erro = document.getElementById("erro");
  var btn = document.getElementById("enviar");
  var btnTxt = document.getElementById("enviar-txt");
  var celular = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent || "");
  // De onde a pessoa veio: /teste/?o=evento, ?o=grupo-melissa...
  var origem = "site";
  try { origem = (new URLSearchParams(location.search).get("o") || "site").slice(0, 60); } catch (e) {}

  var cpf = document.getElementById("cpf");
  cpf.addEventListener("input", function () {
    var d = cpf.value.replace(/\D/g, "").slice(0, 11);
    cpf.value = d.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})\.(\d{3})(\d)/, "$1.$2.$3").replace(/(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
  });
  var zap = document.getElementById("whatsapp");
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
      nome: document.getElementById("nome").value.trim(),
      email: document.getElementById("email").value.trim(),
      whatsapp: zap.value, cpf: cpf.value,
      site: document.getElementById("site").value, origem: origem
    };
    if (dados.nome.length < 3) return mostrarErro("Escreva o seu nome completo.");
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(dados.email)) return mostrarErro("Confira o e-mail: ele parece incompleto.");
    if (zap.value.replace(/\D/g, "").length < 10) return mostrarErro("Confira o WhatsApp, com DDD.");
    if (cpf.value.replace(/\D/g, "").length !== 11) return mostrarErro("Confira o CPF: são 11 números.");
    carregando(true);
    fetch(EDGE, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dados) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        carregando(false);
        j = j || {};
        if (!j.ok) return mostrarErro(j.erro || "Não consegui liberar agora. Tente de novo em instantes.");
        // Guarda o acesso desta aba: a área de membros abre já logada, sem digitar nada.
        if (j.token) { try { sessionStorage.setItem("maestria_membros", JSON.stringify({ token: j.token, cpf: j.cpf })); } catch (e) {} }
        var ate = j.vence_em ? new Date(j.vence_em).toLocaleDateString("pt-BR") : "";
        document.getElementById("ok-titulo").textContent = (j.nome ? j.nome + ", o" : "O") + " seu teste está liberado!";
        var texto = document.getElementById("ok-texto");
        if (celular) {
          texto.textContent = "Vale até " + ate + ". A instalação é no computador: abra lá o e-mail que acabamos de mandar e clique no botão azul.";
          document.getElementById("ok-btn").classList.add("tf-oculto");
        } else {
          texto.textContent = "Vale até " + ate + ". Agora é só instalar: a próxima tela mostra cada passo e onde clicar.";
        }
        document.getElementById("tela-form").classList.add("tf-oculto");
        document.getElementById("tela-ok").classList.remove("tf-oculto");
        document.getElementById("cartao").scrollIntoView({ block: "center" });
      })
      .catch(function () { carregando(false); mostrarErro("Sem conexão agora. Confira a internet e tente de novo."); });
  });
})();
</script>'''

html = '\n'.join([
    cabeca, '<style>', g('css_prev'), g('css_mkt'), g('CSS_COMBO'), CSS_TESTE, '</style>', '',
    NAV, '', HERO, '', g('MARQ'), '', DIFERENCA, '', g('acoes'), '', CTA_MEIO, '',
    g('DIV_PREV'), '', g('prev_rows'), '', g('DIV_MKT'), '', g('mkt_rows'), '', g('sigilo'), '',
    PRECISA, '', DIAS, '', instalacao, '', TESTE, '', FAQ, '', FINAL, '', rodape, '', g('script'), SCRIPT_FORM, '</html>', ''])

# Travas: nada de checkout nem de preço na página do teste, nada de travessão, ids únicos
corpo = html.split('</style>', 1)[1]
for proibido in ('pay.kiwify', 'so-promo', '—', 'R$ 997', 'R$ 697', 'R$ 297', '#pacotes', 'Quero os dois'):
    assert proibido not in corpo, proibido
ids = re.findall(r'\bid="([^"]+)"', html)
assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})
for alvo in set(re.findall(r'href="#([^"]+)"', corpo)):
    assert alvo in ids, 'âncora sem destino: ' + alvo

(RAIZ / 'teste/index.html').write_text(html, encoding='utf-8')
print('ok', len(html), 'bytes')
