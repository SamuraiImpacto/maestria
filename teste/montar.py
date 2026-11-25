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
  header.hero{padding-top:30px;padding-bottom:34px}
  header.hero h1.big{font-size:clamp(2rem,3.5vw,3.15rem);line-height:1.07;max-width:17ch;margin-top:16px}
  header.hero .hero-sub{margin-top:16px;max-width:52ch;font-size:clamp(1rem,1.25vw,1.1rem);line-height:1.55}
  header.hero .term{margin-top:30px}
  .hero-prova{display:flex;gap:12px;align-items:flex-start;margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:14.5px;line-height:1.5;color:var(--muted);text-align:left}
  .hero-prova svg{width:20px;height:20px;flex:0 0 auto;color:var(--green);margin-top:1px}
  .hero-prova b{color:var(--txt)}
  @media (min-width:981px){
    header.hero .wrap{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(0,.98fr);gap:46px;align-items:center;text-align:left}
    header.hero .eyebrow,header.hero h1.big,header.hero .hero-sub{margin-left:0;margin-right:0}
    header.hero .hero-cta,header.hero .hero-fatos{justify-content:flex-start}
    header.hero .term{margin-top:0}
    header.hero .term-body{font-size:13px}
  }
  @media (max-width:980px){.hero-prova{max-width:56ch;margin-left:auto;margin-right:auto}}
  /* tudo o que ela faz */
  .fx-rot{display:flex;align-items:center;gap:12px;margin:40px 0 0;font-size:12.5px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:var(--red-ink);text-align:left}
  .fx-rot::after{content:"";flex:1;height:1px;background:var(--line)}
  .fx{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:16px;text-align:left}
  .fx .cardy{padding:20px;display:flex;flex-direction:column}
  .fx h3{font-size:16.5px;line-height:1.3;margin:0 0 6px}
  .fx p{font-size:14.5px;line-height:1.55;color:var(--muted)}
  .fx-ic{display:inline-flex;width:38px;height:38px;border-radius:50%;background:var(--red-soft);color:var(--red-ink);align-items:center;justify-content:center;margin-bottom:14px;flex:0 0 auto}
  .fx-ic svg{width:20px;height:20px}
  .fx .cardy.topo{grid-column:1/-1;display:grid;grid-template-columns:auto 1fr auto;gap:8px 22px;align-items:center;padding:26px;border-color:rgba(239,39,39,.5);background:linear-gradient(100deg,rgba(239,39,39,.16),rgba(239,39,39,.03) 70%)}
  .fx .cardy.topo .fx-ic{width:54px;height:54px;margin:0}
  .fx .cardy.topo .fx-ic svg{width:27px;height:27px}
  .fx .cardy.topo h3{font-family:var(--serif);font-size:clamp(1.3rem,2.1vw,1.7rem)}
  .fx .cardy.topo p{font-size:15.5px;max-width:64ch}
  .fx-pedido{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px;color:var(--green);background:rgba(70,209,127,.08);border:1px solid rgba(70,209,127,.25);border-radius:10px;padding:10px 14px;max-width:30ch;line-height:1.45}
  .fx-pedido small{display:block;font:700 10.5px var(--sans);letter-spacing:.13em;text-transform:uppercase;color:var(--muted-2);margin-bottom:4px}
  @media (max-width:980px){.fx{grid-template-columns:1fr 1fr}.fx .cardy.topo{grid-template-columns:auto 1fr}.fx-pedido{grid-column:1/-1;max-width:none}}
  @media (max-width:560px){.fx{grid-template-columns:1fr}.fx .cardy.topo{grid-template-columns:1fr}}
  /* quem já usa */
  .deps{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:38px;text-align:left}
  .dep{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:26px 26px 22px;display:flex;flex-direction:column;gap:16px;margin:0}
  .dep::before{content:"\201C";font-family:var(--serif);font-size:54px;line-height:.6;color:var(--red-ink);height:22px}
  .dep blockquote{margin:0;font-size:clamp(1.02rem,1.3vw,1.14rem);line-height:1.58;color:var(--txt)}
  .dep blockquote b{color:var(--red-ink);font-weight:700}
  .dep figcaption{margin-top:auto;padding-top:14px;border-top:1px solid var(--line);font-size:14.5px;color:var(--muted)}
  .dep figcaption b{display:block;color:var(--txt);font-size:15.5px}
  .piloto{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:30px}
  .piloto div{border:1px solid var(--line);border-radius:14px;padding:18px;background:var(--panel)}
  .piloto b{display:block;font-family:var(--serif);font-size:clamp(1.5rem,2.6vw,2.1rem);line-height:1.1;color:var(--txt)}
  .piloto span{display:block;margin-top:6px;font-size:14px;color:var(--muted);line-height:1.45}
  .sub-h{font-size:1.15rem;margin:44px 0 0;text-align:center}
  @media (max-width:800px){.deps,.piloto{grid-template-columns:1fr}}
  /* segurança */
  .seg-grade{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:38px;text-align:left}
  .seg-grade .cardy{padding:24px}
  .seg-grade .cardy h3{font-size:17px}
  .seg-grade .cardy p{font-size:15px}
  .seg-ic{display:inline-flex;width:38px;height:38px;border-radius:50%;background:rgba(70,209,127,.13);color:var(--green);align-items:center;justify-content:center;margin-bottom:14px}
  .seg-ic svg{width:20px;height:20px}
  .seg-vs{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;text-align:left}
  .seg-vs>div{border-radius:14px;padding:22px 24px;border:1px solid var(--line)}
  .seg-vs .outro{background:var(--panel)}
  .seg-vs .nosso{border-color:rgba(70,209,127,.35);background:linear-gradient(180deg,rgba(70,209,127,.07),transparent)}
  .seg-vs .rot{font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--muted-2)}
  .seg-vs .nosso .rot{color:var(--green)}
  .seg-vs ul{list-style:none;margin-top:12px;display:flex;flex-direction:column;gap:9px}
  .seg-vs li{font-size:15px;line-height:1.5;color:var(--muted);display:flex;gap:10px}
  .seg-vs .outro li::before{content:"✕";color:var(--muted-2);font-weight:800}
  .seg-vs .nosso li::before{content:"✓";color:var(--green);font-weight:800}
  .seg-vs .nosso li{color:var(--txt)}
  .seg-nota{margin:20px auto 0;max-width:70ch;color:var(--muted-2);font-size:14px;line-height:1.6}
  /* custo */
  .conta{margin:38px auto 0;max-width:900px;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--panel);text-align:left}
  .conta-l{display:grid;grid-template-columns:1.5fr 1fr;gap:12px;padding:16px 22px;border-top:1px solid var(--line);align-items:center}
  .conta-l:first-child{border-top:0}
  .conta-l b{display:block;font-size:16px}
  .conta-l span{color:var(--muted);font-size:14.5px}
  .conta-l .v{text-align:right;font-weight:800;font-size:1.15rem;color:var(--muted)}
  .conta-l.soma{background:var(--panel-2)}
  .conta-l.soma .v{color:var(--txt)}
  .conta-l.nossa{background:linear-gradient(90deg,rgba(239,39,39,.12),transparent 90%);border-top:2px solid var(--red)}
  .conta-l.nossa .v{color:var(--red-ink);font-size:1.6rem;font-family:var(--serif)}
  .conta-l.nossa .v small{display:block;font:600 13px var(--sans);color:var(--muted)}
  .porque{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px;text-align:left}
  .porque .cardy h3{font-size:16.5px}
  .porque .cardy p{font-size:15px}
  @media (max-width:900px){.seg-grade,.porque{grid-template-columns:1fr 1fr}.seg-vs{grid-template-columns:1fr}}
  @media (max-width:560px){.seg-grade,.porque{grid-template-columns:1fr}.conta-l{grid-template-columns:1fr}.conta-l .v{text-align:left}}
  header.hero .hero-cta{margin-top:22px}
  .hero-fatos{justify-content:center}
  .hero-fatos{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:18px;font-size:14.5px;color:var(--muted)}
  .hero-fatos span{display:inline-flex;align-items:center;gap:8px}
  .hero-fatos b{color:var(--green);font-weight:800}
  .precisa{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:38px;text-align:left}
  .precisa .cardy{padding:24px}
  .precisa .pre-ic{display:inline-flex;width:38px;height:38px;border-radius:50%;background:var(--red-soft);color:var(--red-ink);align-items:center;justify-content:center;margin-bottom:14px}
  .precisa .pre-ic svg{width:20px;height:20px}
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
  /* ===== primeira dobra com o vídeo (25/11/2026): título, vídeo e botão numa tela só ===== */
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
  .hero-vsl .hero-fatos{margin-top:0;justify-content:center}
  .hero-vsl .hv-entra{opacity:0;transform:translateY(14px);animation:hventra .6s cubic-bezier(.2,.7,.2,1) forwards}
  .hero-vsl .hv-entra.d1{animation-delay:.08s}.hero-vsl .hv-entra.d2{animation-delay:.16s}.hero-vsl .hv-entra.d3{animation-delay:.26s}.hero-vsl .hv-entra.d4{animation-delay:.36s}
  @keyframes hventra{to{opacity:1;transform:none}}
  @keyframes hvbrilho{to{background-position:-150% 0}}
  @media (max-width:700px){
    header.hero.hero-vsl{min-height:auto;padding-top:14px}
    .hv-video{width:100%;min-width:0;border-radius:12px}
    .hv-ic{width:52px;height:52px}.hv-ic svg{width:22px;height:22px}.hv-play{gap:10px;font-size:13px}.hv-play span.t{padding:7px 12px;margin-bottom:12px}
    .hero-vsl .btn-lg{width:100%}
  }
  @media (prefers-reduced-motion:reduce){.hero-vsl .hv-entra{animation:none;opacity:1;transform:none}.hv-video{animation:none}.hv-ic,.hv-play{transition:none}}
  #teste{scroll-margin-top:12px}
'''

NAV = '''<nav>
  <div class="wrap nav-in">
    <a class="logo" href="#topo" aria-label="MaestrIA: voltar ao topo"><img class="sym" src="/img/logo-sym.png" alt=""><img class="word" src="/img/logo-word.png" alt="MaestrIA"><span class="sub">Teste grátis</span></a>
    <div class="nav-links">
      <a href="#funcoes">O que ela faz</a>
      <a href="#quem-usa">Quem já usa</a>
      <a href="#seguranca">Segurança</a>
      <a href="#custo">Quanto custa</a>
      <a href="#teste" class="btn btn-red btn-sm nav-cta">Testar 7 dias grátis</a>
    </div>
  </div>
</nav>'''

HERO_ANTIGO = '''<header class="hero" id="topo">
  <div class="hero-art" id="heroArt" aria-hidden="true"><img src="/img/logo-sym.png" alt=""></div>
  <div class="wrap">
    <div class="hero-txt">
      <span class="eyebrow"><i></i>Teste grátis de 7 dias &nbsp;•&nbsp; Previdenciário + Marketing</span>
      <h1 class="big">A pasta do cliente entra. <span class="red">O caso pronto para protocolar sai.</span></h1>
      <p class="hero-sub">Linha do tempo, cálculo, petição, quesitos, procuração e contrato, no seu timbrado. Na aula ao vivo, um caso com 15 documentos, um deles com mais de 300 páginas, ficou montado em <b>22 minutos</b>. E ela ainda faz o conteúdo do seu Instagram.</p>
      <div class="hero-cta">
        <a href="#teste" class="btn btn-red">Quero testar 7 dias grátis</a>
        <a href="#funcoes" class="btn btn-ghost">Ver tudo o que ela faz</a>
      </div>
      <div class="hero-fatos"><span><b>✓</b> Sem cartão</span><span><b>✓</b> Sem cobrança automática</span><span><b>✓</b> Com os seus casos</span></div>
      <p class="hero-prova"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6Z"/><path d="m9 12 2 2 4-4"/></svg><span><b>Feita e testada por previdenciaristas.</b> Já rodou em mais de 30 escritórios na fase piloto.</span></p>
    </div>

    <div class="term" id="term">
      <div class="term-bar">
        <span class="d r"></span><span class="d y"></span><span class="d g"></span>
        <span class="term-title">Você pede. Ela devolve pronto.</span>
      </div>
      <div class="term-body" id="termbody">
        <p class="tl t-cmd"><span class="p">&gt;</span>quero dar entrada no auxílio-acidente desse cliente, faz tudo até o protocolo</p>
        <p class="tl t-resp">Lendo a pasta: carta de concessão, laudo, extrato de contribuições...</p>
        <p class="tl t-resp">Linha do tempo montada. Faltam 2 documentos, já anotados para você pedir.</p>
        <p class="tl t-ok">✓ Cálculo com a memória aberta, mês a mês, em Excel</p>
        <p class="tl t-ok">✓ Petição no seu timbrado, quesitos, procuração e contrato, em Word</p>
        <p class="tl t-ok">✓ Pasta de protocolo pronta, em PDF</p>
        <p class="tl t-cmd"><span class="p">&gt;</span>cria um carrossel sobre quem tem direito ao auxílio-acidente</p>
        <p class="tl t-ok">✓ 8 lâminas com a sua marca e a legenda, dentro das regras da OAB</p>
        <p class="tl t-dim">Exemplo ilustrativo. O advogado revisa tudo antes de usar.<span class="cursor" id="cur"></span></p>
      </div>
    </div>
  </div>
</header>'''

# Primeira dobra (25/11/2026, pedido do Samurai): só o título, o vídeo e o botão, tudo numa tela.
# O botão desce para a ficha de cadastro (#teste), que passa a ser a segunda dobra.
HERO = '''<header class="hero hero-vsl" id="topo">
  <div class="hero-art" id="heroArt" aria-hidden="true"><img src="/img/logo-sym.png" alt=""></div>
  <div class="wrap">
    <span class="eyebrow hv-entra"><i></i>Teste grátis de 7 dias &nbsp;•&nbsp; Previdenciário + Marketing</span>
    <h1 class="big hv-entra d1">Uma equipe de assistentes jurídicos <span class="red">dentro do seu computador.</span></h1>
    <p class="hv-sub hv-entra d2">Dê o play: em 3 minutos você vê um caso sair da pasta do cliente pronto para protocolar. Você só revisa e assina.</p>
    <div class="hv-video hv-entra d3" id="hvVideo">
      <video id="vsl" preload="none" playsinline poster="/teste/vsl-capa.jpg" src="/teste/vsl-maestria.mp4" aria-label="Vídeo: o que é a MaestrIA, em 3 minutos"></video>
      <button type="button" class="hv-play" id="hvPlay" aria-label="Assistir ao vídeo com som"><span class="hv-ic"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg></span><span class="t">Assistir com som &nbsp;•&nbsp; 3 min</span></button>
    </div>
    <div class="hv-cta hv-entra d4">
      <a href="#teste" class="btn btn-red btn-lg">Quero testar 7 dias grátis</a>
      <div class="hero-fatos"><span><b>✓</b> Sem cartão</span><span><b>✓</b> Sem cobrança automática</span><span><b>✓</b> Com os seus casos</span></div>
    </div>
  </div>
</header>'''

I_CADEADO = '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
I_PASTA = '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
I_ESCUDO = '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6Z"/><path d="m9 12 2 2 4-4"/>'
I_OLHO = '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'
I_MOEDA = '<circle cx="12" cy="12" r="9"/><path d="M12 7v10"/><path d="M15 9.5h-4.5a1.75 1.75 0 0 0 0 3.5h3a1.75 1.75 0 0 1 0 3.5H9"/>'
I_LUPA = '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'
I_IMAGEM = '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/>'
I_PINO = '<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>'
sem_classe = lambda d: KI(d).replace('class="ki" ', '')
fx = lambda ic, h, p: f'      <div class="cardy"><span class="fx-ic">{sem_classe(ic)}</span><h3>{h}</h3><p>{p}</p></div>'

FX_PREV = [
    (g('I_CALC'), 'Cálculo com a memória aberta', 'RMI, auxílio-acidente, atrasados e tempo especial. Mês a mês, em Excel, com a fonte de cada índice.'),
    (g('I_DOC'), 'Petição no seu timbrado', 'Escrita do jeito do seu escritório, com um revisor treinado nos seus critérios.'),
    (g('I_BALANCA'), 'Jurisprudência que existe', 'Cada decisão é conferida no CNJ e no site do tribunal. O que não existe, ela joga fora.'),
    (I_LUPA, 'Auditor de CNIS', 'Vínculo faltando e contribuição não computada, apontados em minutos.'),
    (I_ESCUDO, 'Perícia de ponta a ponta', 'Quesitos, impugnação de PPP e de laudo, e o cliente preparado para o dia.'),
    (I_CHECK, 'Qualificador de auxílio-acidente', 'Acidente, sequela e qualidade de segurado. Tem direito ou não tem? A resposta sai na hora.'),
    (g('I_BARRA'), 'Jurimetria por vara', 'Procedência e acordo com dados oficiais do CNJ, antes de você ajuizar.'),
    (g('I_SINO'), 'Intimações pela sua OAB', 'As publicações do dia, com o vencimento de cada prazo já calculado.'),
]
FX_MKT = [
    (g('I_ESTRELA'), 'Conteúdo com a sua voz', 'Reels, carrosséis, estáticos e artigos que soam como você, e não como robô.'),
    (g('I_VIDEO'), 'Edição de vídeo', 'Você grava no celular. Ela tira pausa e gagueira, põe legenda e animação.'),
    (I_IMAGEM, 'Arte pronta', 'Imagens com a sua marca, ou o design direto na sua conta do Canva.'),
    (g('I_GRADE'), 'Calendário do mês inteiro', 'A pauta da sua área para 30 dias, em minutos.'),
    (g('I_GLOBO'), 'Site do escritório no ar', 'Com blog, no seu domínio, hospedado de graça.'),
    (g('I_RAIO'), 'Página de campanha', 'Pronta para receber o anúncio, com Pixel e botão de WhatsApp.'),
    (I_PINO, 'Google Meu Negócio', 'Da criação à rotina, para quem procura advogado perto de casa.'),
    (I_CADEADO, 'Filtro do Provimento 205', 'Tudo passa pelas regras da OAB antes de chegar em você.'),
]
NL = chr(10)
FUNCOES = f'''<section id="funcoes">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_RAIO)}<span>Tudo o que ela faz</span></span>
    <h2 class="sec reveal">Você pede em português. <span class="red">Ela entrega pronto.</span></h2>
    <p class="lead reveal">Sem comando difícil e sem tela nova para aprender. Você escreve o que precisa, como falaria com um estagiário, e recebe em Word, Excel e PDF.</p>
    <div class="fx-rot reveal">Previdenciário</div>
    <div class="fx reveal">
      <div class="cardy topo">
        <span class="fx-ic">{sem_classe(I_PASTA)}</span>
        <div><h3>O caso completo, do zero ao protocolo</h3><p>Ela lê a pasta do cliente, monta a linha do tempo, aponta o documento que falta, mostra os caminhos possíveis, calcula, escreve a petição, os quesitos, a procuração, a declaração e o contrato. No fim, entrega a pasta de protocolo em PDF.</p></div>
        <div class="fx-pedido"><small>Você escreve</small>faz tudo desse cliente até o protocolo</div>
      </div>
{NL.join(fx(*x) for x in FX_PREV)}
    </div>
    <div class="fx-rot reveal">Marketing</div>
    <div class="fx reveal">
{NL.join(fx(*x) for x in FX_MKT)}
    </div>
    <div class="cta-meio" style="padding-top:34px">
      <a href="#teste" class="btn btn-red btn-lg reveal">Quero testar tudo isso por 7 dias</a>
      <p class="reveal">Tudo liberado no teste. Sem cartão.</p>
    </div>
  </div>
</section>'''

dep = lambda fala, nome, quem: f'      <figure class="dep"><blockquote>{fala}</blockquote><figcaption><b>{nome}</b>{quem}</figcaption></figure>'
DEPOIMENTOS = f'''<section id="quem-usa" style="padding-top:0">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_ESTRELA)}<span>Quem já usa</span></span>
    <h2 class="sec reveal">Feita e testada por previdenciaristas. <span class="red">Mais de 30 escritórios</span> na fase piloto.</h2>
    <p class="lead reveal">Antes de abrir este teste, a MaestrIA rodou em escritório de verdade, com caso de verdade. As falas abaixo são de advogados que usam, ditas na aula ao vivo de 11 de novembro de 2026.</p>
    <div class="deps reveal">
{dep('Teve uma cliente que chegou num dia de manhã. No outro dia, a gente já tinha mandado o protocolo para ela. <b>Literalmente em 24 horas.</b> Isso jamais na história da humanidade iria acontecer manualmente.', 'Jean Piaça', 'Advogado previdenciarista')}
{dep('Antes ficava ali 30 dias esperando para sair a inicial. Agora, se está tudo na mão, <b>sai no dia, com certeza.</b> Eu consigo fazer muito mais sem contratar ninguém.', 'Cleice Wiedthauger', 'Advogada previdenciarista, auxílio-acidente')}
{dep('Se tem uma coisa que eu não gosto é gravar vídeo. Abri a câmera, falei o que tinha que falar e coloquei na MaestrIA. Ela tirou a gagueira, tirou tudo. <b>Não parecia eu, parecia uma jornalista falando.</b>', 'Érika Neves', 'Advogada de família, usa a parte de Marketing')}
{dep('A MaestrIA me ajudou muito. <b>Em questão de horas</b> está pronta toda a documentação, as petições. Eu não tinha habilidade com tecnologia. Agora estou aprendendo e usando, pelo bem do escritório.', 'Joel Sidney de Christo Machado', 'Advogado, atua sozinho')}
    </div>
    <p class="seg-nota reveal">São relatos da experiência de cada escritório, e não promessa de resultado. Cada caso depende dos documentos e da revisão do advogado.</p>
  </div>
</section>'''

DIFERENCA = g('DIFERENCA')
DIFERENCA = DIFERENCA.replace('O mesmo pedido. <span class="red">Duas respostas diferentes</span>.',
                              'O que a MaestrIA faz que a <span class="red">IA comum não faz</span>.')
DIFERENCA = DIFERENCA.replace('O Claude sozinho conversa muito bem. Mas ele não conhece o seu escritório, não tem o motor de cálculo do INSS e não confere se a decisão que citou existe. E a cada conversa nova, começa do zero.',
                              'A MaestrIA funciona dentro do Claude, um aplicativo de inteligência artificial. Sozinho, o Claude conversa muito bem, mas não conhece o seu escritório, não tem o motor de cálculo do INSS e não confere se a decisão que citou existe. Veja a diferença, pedido por pedido.')
DIFERENCA = DIFERENCA.replace('É o mesmo Claude que você já assina. A MaestrIA se instala dentro dele: não é outro site, outro login nem outra tela.',
                              'A MaestrIA se instala dentro do Claude: não é outro site, outro login nem outra tela para aprender.')
assert 'IA comum não faz' in DIFERENCA and 'pedido por pedido' in DIFERENCA

I_CADEADO = '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
I_PASTA = '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
I_ESCUDO = '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6Z"/><path d="m9 12 2 2 4-4"/>'
I_OLHO = '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'
I_MOEDA = '<circle cx="12" cy="12" r="9"/><path d="M12 7v10"/><path d="M15 9.5h-4.5a1.75 1.75 0 0 0 0 3.5h3a1.75 1.75 0 0 1 0 3.5H9"/>'
sem_classe = lambda d: KI(d).replace('class="ki" ', '')

SEGURANCA = f'''<section id="seguranca" style="padding-top:0">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_CADEADO)}<span>Segurança e sigilo</span></span>
    <h2 class="sec reveal">Os documentos do seu cliente ficam <span class="red">no seu computador</span>.</h2>
    <p class="lead reveal">Laudo médico, CPF e histórico de contribuição são o dado mais sensível da advocacia. Por isso a MaestrIA não é um site onde você envia arquivo: é uma ferramenta instalada na sua máquina.</p>
    <div class="seg-grade reveal">
      <div class="cardy"><span class="seg-ic">{sem_classe(I_PASTA)}</span><h3>Nada de cliente vem para nós</h3><p>O que a MaestrIA confere pela internet é só o código da sua licença e o nome do computador. Nome de cliente, CPF, laudo e petição não passam por servidor nosso.</p></div>
      <div class="cardy"><span class="seg-ic">{sem_classe(I_CADEADO)}</span><h3>A IA roda na sua conta</h3><p>A inteligência é a do Claude, da Anthropic, usada pela sua própria assinatura. O que a IA lê para trabalhar segue as regras e as configurações de privacidade da sua conta lá, que você controla.</p></div>
      <div class="cardy"><span class="seg-ic">{sem_classe(I_ESCUDO)}</span><h3>Não inventa jurisprudência</h3><p>Cada decisão citada é conferida na base do CNJ e no site do tribunal. O que não se confirma fica fora da peça, e ela avisa.</p></div>
      <div class="cardy"><span class="seg-ic">{sem_classe(I_OLHO)}</span><h3>Você vê de onde saiu cada dado</h3><p>O cálculo vem com a memória aberta, mês a mês, e a fonte de cada índice. A leitura dos documentos aponta a página de onde tirou a informação.</p></div>
      <div class="cardy"><span class="seg-ic">{sem_classe(I_CHECK)}</span><h3>Nada sai sem a sua revisão</h3><p>A MaestrIA não protocola, não envia mensagem e não fala com o seu cliente. Ela entrega o trabalho pronto para você revisar, decidir e assinar.</p></div>
      <div class="cardy"><span class="seg-ic">{sem_classe(g('I_BALANCA'))}</span><h3>Dentro das regras da OAB</h3><p>O conteúdo de marketing passa por um filtro do Provimento 205/2021 antes de chegar em você: sem promessa de resultado e sem captação indevida.</p></div>
    </div>
    <p class="seg-nota reveal">Transparência: para a IA trabalhar, o texto dos documentos é lido pelo Claude, na sua conta. A MaestrIA não guarda cópia de nada disso.</p>
  </div>
</section>'''

CUSTO = f'''<section id="custo" style="padding-top:0">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_MOEDA)}<span>A conta</span></span>
    <h2 class="sec reveal">Quanto custa, e por que sai <span class="red">mais barato</span> do que contratar cada coisa separada.</h2>
    <p class="lead reveal">Para ter o que a MaestrIA entrega, o escritório costuma pagar vários fornecedores, quase todos com mensalidade. Veja a soma em um ano.</p>
    <div class="conta reveal">
      <div class="conta-l"><div><b>Social media terceirizado</b><span>R$ 800 a R$ 2.500 por mês, para postar no seu Instagram</span></div><div class="v">R$ 10 a 30 mil</div></div>
      <div class="conta-l"><div><b>Site feito por web designer</b><span>pago uma vez, e você depende dele para mexer</span></div><div class="v">R$ 3 a 8 mil</div></div>
      <div class="conta-l"><div><b>Plataforma de jurimetria</b><span>cerca de R$ 300 por mês</span></div><div class="v">R$ 3,6 mil</div></div>
      <div class="conta-l"><div><b>Cálculo previdenciário feito na mão</b><span>2 a 3 horas de trabalho repetitivo por caso, toda vez</span></div><div class="v">as suas horas</div></div>
      <div class="conta-l soma"><div><b>Em um ano, separado</b><span>sem contar as horas do cálculo e da petição</span></div><div class="v">R$ 16 a 41 mil</div></div>
      <div class="conta-l nossa"><div><b>MaestrIA Previdenciário + Marketing</b><span>os dois pacotes, 12 meses, com as atualizações</span></div><div class="v">R$ 997<small>menos de R$ 84 por mês</small></div></div>
    </div>
    <h3 class="sub-h reveal">E a diferença para um sistema jurídico online comum</h3>
    <div class="seg-vs reveal">
      <div class="outro">
        <span class="rot">Sistema jurídico online comum</span>
        <ul>
          <li>Você envia os documentos do cliente para o servidor da empresa.</li>
          <li>Os casos ficam guardados em um banco de dados que não é seu.</li>
          <li>Se você cancela, depende da empresa para tirar tudo de lá.</li>
          <li>Mensalidade por usuário, para sempre.</li>
        </ul>
      </div>
      <div class="nosso">
        <span class="rot">MaestrIA</span>
        <ul>
          <li>Os arquivos ficam em pastas suas, no seu computador.</li>
          <li>A MaestrIA não tem servidor que recebe documento de cliente.</li>
          <li>Se você sair, tudo o que foi feito continua com você, em Word, Excel e PDF.</li>
          <li>Sem mensalidade por usuário.</li>
        </ul>
      </div>
    </div>
    <div class="porque reveal">
      <div class="cardy"><h3>Não tem mensalidade por usuário</h3><p>A licença é do escritório, por 12 meses, em até 3 computadores. Não cresce a conta a cada pessoa que usa.</p></div>
      <div class="cardy"><h3>Não mantemos servidor com os seus casos</h3><p>Como tudo roda no seu computador, não existe o custo de guardar e processar os seus documentos em um sistema nosso. Esse custo não vai para o seu preço.</p></div>
      <div class="cardy"><h3>A inteligência você paga direto</h3><p>A assinatura do Claude é sua, contratada na Anthropic, sem intermediário cobrando por cima. É o único custo fora da MaestrIA.</p></div>
    </div>
    <p class="seg-nota reveal">Valores de mercado são referências médias e variam por cidade e fornecedor. O preço da MaestrIA é o da página oficial do pacote. Durante o teste de 7 dias você não paga nada à MaestrIA.</p>
  </div>
</section>'''

CTA_MEIO = '''<section class="cta-meio">
  <div class="wrap">
    <a href="#teste" class="btn btn-red btn-lg reveal">Quero ver isso no meu escritório</a>
    <p class="reveal">7 dias grátis, sem cartão. Você libera o teste em um minuto.</p>
  </div>
</section>'''

PRECISA = f'''<section id="precisa">
  <div class="wrap sec-center">
    <span class="kicker reveal">{KI(I_CHECK)}<span>Antes de começar</span></span>
    <h2 class="sec reveal">O que você precisa ter para <span class="red">fazer o teste</span>.</h2>
    <p class="lead reveal">São só três coisas. Se faltar alguma, a área de membros mostra como resolver, com a imagem de cada tela.</p>
    <div class="precisa reveal">
      <div class="cardy">
        <span class="pre-ic">{KI(I_PC).replace('class="ki"', '')}</span>
        <h3>1. Um computador</h3>
        <p>Windows ou Mac. A MaestrIA trabalha com os arquivos do seu computador, por isso <b>não funciona no celular</b>. Não precisa ser uma máquina potente.</p>
      </div>
      <div class="cardy red-edge">
        <span class="pre-ic">{KI(I_ESTRELA).replace('class="ki"', '')}</span>
        <h3>2. O aplicativo Claude, com assinatura</h3>
        <p>O Claude é o aplicativo de inteligência artificial onde a MaestrIA se instala. Ele tem uma <b>assinatura própria</b>, contratada direto em <a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a>. É o único custo durante o teste, e você continua com ele mesmo se não ficar com a MaestrIA.</p>
      </div>
      <div class="cardy">
        <span class="pre-ic">{KI(I_RELOGIO).replace('class="ki"', '')}</span>
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
          <p class="sub">Só nome, e-mail e WhatsApp. O acesso chega na hora.</p>
          <form id="f" novalidate>
            <div class="tf-campo"><label for="nome">Nome completo</label><input type="text" id="nome" name="nome" autocomplete="name" maxlength="120" required></div>
            <div class="tf-campo"><label for="email">E-mail</label><input type="email" id="email" name="email" autocomplete="email" maxlength="160" required></div>
            <div class="tf-campo"><label for="whatsapp">WhatsApp com DDD</label><input type="tel" id="whatsapp" name="whatsapp" autocomplete="tel" inputmode="tel" placeholder="(11) 99999-9999" maxlength="20" required></div>
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
    ('Quanto custa depois do teste?',
     'O pacote Previdenciário + Marketing custa R$ 997 por 12 meses, com as atualizações do período. Não é mensalidade por usuário. Fora isso, só a assinatura do Claude, que você paga direto à Anthropic.'),
    ('Os dados dos meus clientes ficam seguros?',
     'Os arquivos ficam em pastas suas, no seu computador. A MaestrIA não tem servidor que recebe documento de cliente: pela internet ela confere só o código da licença e o nome do computador. Para trabalhar, a inteligência artificial do Claude lê o texto dos documentos, pela sua própria conta, seguindo as configurações de privacidade que você controla lá.'),
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
    <h2 class="reveal">Sete dias, com os seus casos, <span class="red">sem pagar nada</span>.</h2>
    <p class="reveal">Instale hoje e rode o primeiro caso ainda hoje. Se não for para você, é só não fazer nada: o teste pausa sozinho.</p>
    <a href="#teste" class="btn btn-red btn-lg reveal">Quero testar por 7 dias</a>
    <p class="reveal" style="margin-top:16px;font-size:15px">Já decidiu e prefere comprar direto? <a href="/prev-marketing/#pacotes" style="color:var(--red-ink)">Ver o pacote por R$ 997</a>.</p>
    <p class="cta-meta reveal"><span>Sem cartão</span><span>Os dois pacotes completos</span><span>No seu computador</span><span>Você decide no fim</span></p>
  </div>
</section>'''

rodape = g('rodape')
rodape = rodape.replace('<a href="#pacotes">O pacote</a>', '<a href="#teste">Testar 7 dias</a>')
# O logo desta página volta ao topo dela, e não à página de todas as áreas.
assert rodape.count('<a class="logo" href="/"') == 1
rodape = rodape.replace('<a class="logo" href="/"', '<a class="logo" href="#topo"')

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
  f.addEventListener("input", function () { if (!comecou) { comecou = true; contar("formulario"); } });

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
      whatsapp: zap.value,
      site: document.getElementById("site").value, origem: origem
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

SCRIPT_VSL = '''<script>
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
    var alvo = document.getElementById("teste"); if (alvo) alvo.scrollIntoView({ behavior: "smooth" });
  });
})();
</script>'''

html = '\n'.join([
    cabeca, '<style>', g('css_prev'), g('css_mkt'), g('CSS_COMBO'), CSS_TESTE, '</style>', '',
    NAV, '', HERO, '', TESTE, '', g('MARQ'), '', FUNCOES, '', DEPOIMENTOS, '', g('acoes'), '', CTA_MEIO, '',
    g('DIV_PREV'), '', g('prev_rows'), '', g('DIV_MKT'), '', g('mkt_rows'), '', SEGURANCA, '',
    PRECISA, '', DIAS, '', instalacao, '', DIFERENCA, '', CUSTO, '', FAQ, '', FINAL, '', rodape, '', g('script'), SCRIPT_FORM, SCRIPT_VSL, '</html>', ''])

# Travas: nada de checkout nem de preço na página do teste, nada de travessão, ids únicos
corpo = html.split('</style>', 1)[1]
for proibido in ('pay.kiwify', 'so-promo', '—', 'R$ 697', 'R$ 297', 'href="#pacotes"', 'Quero os dois', 'servidor de terceiros'):
    assert proibido not in corpo, proibido
ids = re.findall(r'\bid="([^"]+)"', html)
assert len(ids) == len(set(ids)), sorted({i for i in ids if ids.count(i) > 1})
for alvo in set(re.findall(r'href="#([^"]+)"', corpo)):
    assert alvo in ids, 'âncora sem destino: ' + alvo

(RAIZ / 'teste/index.html').write_text(html, encoding='utf-8')
print('ok', len(html), 'bytes')
