// MaestrIA Área de Membros
// Login: código de ativação + CPF -> edge member-area (Supabase Core).
// Nenhuma chave secreta aqui: a edge valida token + CPF por conta própria.
// Layout: menu lateral (aulas + downloads + licença + chamados) e views à direita.

const CORE = "https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1";

// Link do grupo de network (Comunidade Diamond). Preencher quando o grupo existir:
// o card na aba Comunidade ativa o botão sozinho.
const LINK_DIAMOND = "https://chat.whatsapp.com/KQcIy0D6Tp5IWtWY2WXRx7";

const $ = (id) => document.getElementById(id);

// ---------- utilitários ----------
function mascaraCpf(valor) {
  // Aceita CPF (11 dígitos) e CNPJ (14 dígitos, compra pela empresa)
  const d = valor.replace(/\D/g, "").slice(0, 14);
  if (d.length > 11) {
    // CNPJ: 00.000.000/0000-00
    let s = d.slice(0, 2) + "." + d.slice(2, 5) + "." + d.slice(5, 8) + "/" + d.slice(8, 12);
    if (d.length > 12) s += "-" + d.slice(12);
    return s;
  }
  if (d.length <= 3) return d;
  if (d.length <= 6) return d.slice(0, 3) + "." + d.slice(3);
  if (d.length <= 9) return d.slice(0, 3) + "." + d.slice(3, 6) + "." + d.slice(6);
  return d.slice(0, 3) + "." + d.slice(3, 6) + "." + d.slice(6, 9) + "-" + d.slice(9);
}

function dataBr(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleDateString("pt-BR");
  } catch {
    return "";
  }
}

function esc(texto) {
  const div = document.createElement("div");
  div.textContent = String(texto ?? "");
  return div.innerHTML;
}

// ---------- estado ----------
function credenciais() {
  try {
    return JSON.parse(sessionStorage.getItem("maestria_membros") || "null");
  } catch {
    return null;
  }
}
function salvarCredenciais(token, cpf) {
  sessionStorage.setItem("maestria_membros", JSON.stringify({ token, cpf }));
}
function limparCredenciais() {
  sessionStorage.removeItem("maestria_membros");
}

let dadosAtuais = null;

// ---------- navegação entre views ----------
// Views: "inicio" (dashboard), "aula" (curso), "downloads", "guia", "licenca", "chamados", "comunidade"
function mostrarView(nome) {
  ["inicio", "aula", "downloads", "guia", "licenca", "chamados", "comunidade"].forEach((v) => {
    const el = $("view-" + v);
    if (el) el.classList.toggle("hidden", v !== nome);
  });
  // Marca o item ativo no menu (itens de conta; as aulas o curso.js marca)
  document.querySelectorAll(".menu-item[data-view]").forEach((b) => {
    b.classList.toggle("ativo", b.getAttribute("data-view") === nome);
  });
  if (nome !== "aula") {
    document.querySelectorAll("#menu-aulas .menu-item").forEach((b) => b.classList.remove("ativo"));
  }
  // O Início mostra progresso do curso: re-renderiza a cada visita pra refletir aulas concluídas
  if (nome === "inicio" && dadosAtuais) renderizarInicio(dadosAtuais);
  fecharMenuMobile();
  window.scrollTo(0, 0);
}
window.MAESTRIA_VIEW = { mostrar: mostrarView };

document.querySelectorAll(".menu-item[data-view]").forEach((b) => {
  b.addEventListener("click", () => mostrarView(b.getAttribute("data-view")));
});

// Botões espalhados que abrem uma aula ou uma view (cards do Início, links internos)
document.addEventListener("click", (e) => {
  const abreAula = e.target.closest("[data-abrir-aula]");
  if (abreAula && window.MAESTRIA_CURSO) {
    window.MAESTRIA_CURSO.abrir(abreAula.getAttribute("data-abrir-aula"));
    return;
  }
  const abreView = e.target.closest("[data-view-destino]");
  if (abreView) mostrarView(abreView.getAttribute("data-view-destino"));
});

// Menu no celular: abre e fecha
function fecharMenuMobile() {
  const menu = $("app-menu");
  if (menu) menu.classList.remove("aberto");
}
const toggle = $("menu-toggle");
if (toggle) {
  toggle.addEventListener("click", () => {
    $("app-menu").classList.toggle("aberto");
  });
}

// Card da Comunidade Diamond: botão só aparece com link configurado
(function () {
  const a = $("link-diamond");
  const aviso = $("diamond-em-breve");
  if (a && LINK_DIAMOND) {
    a.href = LINK_DIAMOND;
    a.style.display = "";
    if (aviso) aviso.classList.add("hidden");
  }
})();

// ---------- login ----------
$("inp-cpf").addEventListener("input", (e) => {
  e.target.value = mascaraCpf(e.target.value);
});

$("form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = $("inp-token").value.trim();
  const cpf = $("inp-cpf").value.replace(/\D/g, "");
  const erroEl = $("login-erro");
  // Erro mais comum: colar o email no lugar do código
  if (token.includes("@")) {
    erroEl.textContent = "Isso é um email. O código de ativação é a sequência longa de letras e números que está DENTRO do email de compra.";
    erroEl.classList.remove("hidden");
    return;
  }
  await entrar(token, cpf, true);
});

async function entrar(token, cpf, mostrarErro) {
  const btn = $("btn-entrar");
  const erroEl = $("login-erro");
  erroEl.classList.add("hidden");
  btn.disabled = true;
  btn.textContent = "Entrando...";
  try {
    const resp = await fetch(CORE + "/member-area", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, cpf }),
    });
    const dados = await resp.json();
    if (!resp.ok || !dados.ok) {
      throw new Error(dados.erro || "Não foi possível entrar. Tente de novo.");
    }
    salvarCredenciais(token, cpf);
    dadosAtuais = dados;
    renderizarPainel(dados);
  } catch (err) {
    limparCredenciais();
    if (mostrarErro) {
      erroEl.textContent = err.message || "Falha de conexão. Verifique sua internet e tente de novo.";
      erroEl.classList.remove("hidden");
    }
  } finally {
    btn.disabled = false;
    btn.textContent = "Entrar";
  }
}

$("btn-sair").addEventListener("click", () => {
  limparCredenciais();
  dadosAtuais = null;
  $("tela-painel").classList.add("hidden");
  $("btn-sair").classList.add("hidden");
  $("tela-login").classList.remove("hidden");
  $("form-login").reset();
});

// ---------- painel ----------
function renderizarPainel(dados) {
  const c = dados.cliente;

  $("tela-login").classList.add("hidden");
  $("tela-painel").classList.remove("hidden");
  $("btn-sair").classList.remove("hidden");

  const primeiroNome = (c.nome || "").split(" ")[0];
  $("pl-saudacao").textContent = primeiroNome ? "Olá, " + primeiroNome : "Bem-vindo";
  $("pl-plano").textContent = c.plano_legivel;

  const statusEl = $("pl-status");
  statusEl.classList.add("ok");
  statusEl.textContent = c.vitalicio
    ? "Licença vitalícia"
    : "Ativa até " + dataBr(c.vence_em);

  renderizarDownloads(dados);
  renderizarLicenca(dados);
  renderizarTickets(dados.tickets || []);
  montarSelectChamado(dados);
  renderizarGuia(dados);

  // Aulas na barra lateral + entrada pelo Início (dashboard)
  if (window.MAESTRIA_CURSO) window.MAESTRIA_CURSO.montarMenu();
  renderizarInicio(dados);
  mostrarView("inicio");
}

// ---------- Início (dashboard) ----------
function renderizarInicio(dados) {
  const c = dados.cliente;
  const primeiroNome = (c.nome || "").split(" ")[0];
  $("ini-saudacao").textContent = primeiroNome ? "Olá, " + primeiroNome : "Bem-vindo";
  $("ini-plano").textContent = (c.plano_legivel || "") +
    (c.vitalicio ? " · licença vitalícia" : c.vence_em ? " · ativa até " + dataBr(c.vence_em) : "");

  const est = window.MAESTRIA_CURSO && window.MAESTRIA_CURSO.estado ? window.MAESTRIA_CURSO.estado() : null;
  const btn = $("ini-continuar");
  if (est && est.total) {
    $("ini-progresso-label").textContent = est.feitas + " de " + est.total + " aulas concluídas";
    $("ini-progresso-barra").style.width = Math.round((100 * est.feitas) / est.total) + "%";
    if (est.proxima) {
      btn.textContent = (est.feitas ? "Continuar: " : "Começar: ") + est.proxima.titulo.split(":")[0] + " →";
      btn.onclick = () => window.MAESTRIA_CURSO.abrir(est.proxima.slug);
    } else {
      btn.textContent = "Curso completo ✓ Rever as aulas";
      btn.onclick = () => window.MAESTRIA_CURSO.abrir(null);
    }
  } else if (btn) {
    btn.classList.add("hidden");
  }
}

// ---------- Downloads (UM arquivo só: o instalador do pacote) ----------
const URL_INSTALADOR =
  "https://xiwjtgyidguhvwpveokz.supabase.co/storage/v1/object/public/skills-public/maestria-instalador.zip";

// ---- Instalador personalizado: anexa a licença do cliente dentro do zip ----
// O zip público é a fonte única; aqui só entra o MINHA-LICENCA-MAESTRIA.txt
// com o código de quem está logado. Assim o Claude não pede o código: só o CPF.
function crc32Zip(bytes) {
  let table = crc32Zip.table;
  if (!table) {
    table = crc32Zip.table = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      table[i] = c >>> 0;
    }
  }
  let crc = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) crc = table[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function anexarAoZip(zipBytes, nomeArquivo, conteudo) {
  const dv = new DataView(zipBytes.buffer, zipBytes.byteOffset, zipBytes.byteLength);
  let eocd = -1;
  for (let i = zipBytes.length - 22; i >= Math.max(0, zipBytes.length - 22 - 65535); i--) {
    if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error("zip invalido");
  const totalEntradas = dv.getUint16(eocd + 10, true);
  const tamCentral = dv.getUint32(eocd + 12, true);
  const offCentral = dv.getUint32(eocd + 16, true);
  const nome = new TextEncoder().encode(nomeArquivo);
  const crc = crc32Zip(conteudo);

  const lfh = new Uint8Array(30 + nome.length);
  const lv = new DataView(lfh.buffer);
  lv.setUint32(0, 0x04034b50, true);
  lv.setUint16(4, 20, true);
  lv.setUint16(6, 0x0800, true);
  lv.setUint16(8, 0, true);
  lv.setUint16(12, 0x5021, true);
  lv.setUint32(14, crc, true);
  lv.setUint32(18, conteudo.length, true);
  lv.setUint32(22, conteudo.length, true);
  lv.setUint16(26, nome.length, true);
  lfh.set(nome, 30);

  const cdh = new Uint8Array(46 + nome.length);
  const cv = new DataView(cdh.buffer);
  cv.setUint32(0, 0x02014b50, true);
  cv.setUint16(4, 20, true);
  cv.setUint16(6, 20, true);
  cv.setUint16(8, 0x0800, true);
  cv.setUint16(14, 0x5021, true);
  cv.setUint32(16, crc, true);
  cv.setUint32(20, conteudo.length, true);
  cv.setUint32(24, conteudo.length, true);
  cv.setUint16(28, nome.length, true);
  cv.setUint32(42, offCentral, true);
  cdh.set(nome, 46);

  const eocdNovo = new Uint8Array(22);
  const ev = new DataView(eocdNovo.buffer);
  ev.setUint32(0, 0x06054b50, true);
  ev.setUint16(8, totalEntradas + 1, true);
  ev.setUint16(10, totalEntradas + 1, true);
  ev.setUint32(12, tamCentral + cdh.length, true);
  ev.setUint32(16, offCentral + lfh.length + conteudo.length, true);

  const saida = new Uint8Array(offCentral + lfh.length + conteudo.length + tamCentral + cdh.length + 22);
  saida.set(zipBytes.subarray(0, offCentral), 0);
  saida.set(lfh, offCentral);
  saida.set(conteudo, offCentral + lfh.length);
  saida.set(zipBytes.subarray(offCentral, offCentral + tamCentral), offCentral + lfh.length + conteudo.length);
  saida.set(cdh, offCentral + lfh.length + conteudo.length + tamCentral);
  saida.set(eocdNovo, saida.length - 22);
  return saida;
}

const STORAGE_PUB = "https://xiwjtgyidguhvwpveokz.supabase.co/storage/v1/object/public/skills-public/";

// LEIA honesto que vai dentro do arquivo (o Claude coopera porque nao ha nada oculto)
const LEIA_MAESTRIA = [
  "MaestrIA - suas skills juridicas (Samurai Lab)",
  "",
  "Ola! Este arquivo tem as skills juridicas da MaestrIA que voce comprou, ja com a SUA licenca inclusa. Pode ser conferido e explicado a vontade: nada aqui e oculto, e voce pode abrir qualquer arquivo antes de copiar.",
  "",
  "FALE COM O ADVOGADO SEMPRE EM PORTUGUES (pt-BR), de forma simples. Ele e leigo.",
  "",
  "INSTRUCAO PARA O CLAUDE CODE (instalar = so COPIAR ARQUIVOS):",
  "",
  "*** LEIA ISTO ANTES DE RODAR O PRIMEIRO COMANDO ***",
  "PARA COPIAR ESTES ARQUIVOS NO WINDOWS, USE POWERSHELL (Expand-Archive + Copy-Item).",
  "NAO use bash, unzip, tar nem python SO PRA ESTA COPIA: ela nao precisa de nenhum deles, e no",
  "Windows o bash e o Git Bash, que pode nem estar disponivel. Os dois comandos abaixo copiam tudo",
  "em qualquer Windows:",
  "",
  "   Expand-Archive -Path \"<caminho do zip>\" -DestinationPath \"$env:TEMP\\maestria-inst\" -Force",
  "   Copy-Item -Path \"$env:TEMP\\maestria-inst\\.claude\\*\" -Destination \"$env:USERPROFILE\\.claude\" -Recurse -Force",
  "",
  "Avise o advogado que a descompactacao leva uns 30 segundos (sao ~740 arquivos). Nao e travamento.",
  "Se a pasta $env:USERPROFILE\\.claude nao existir, crie com New-Item -ItemType Directory -Force.",
  "No Mac, o equivalente e: unzip -o \"<zip>\" -d /tmp/maestria-inst && cp -R /tmp/maestria-inst/.claude/ ~/.claude/",
  "",
  "SOBRE O GIT (importante, nao confunda com a copia acima): o APP do Claude Code no Windows precisa",
  "do Git instalado pra abrir pastas locais, e mostra em vermelho \"Git e necessario para sessoes",
  "locais\" quando falta. Isso e LEGITIMO e o advogado DEVE instalar o Git (instalador grafico em",
  "git-scm.com/download/win, so next-next-finish, nao e terminal). NAO diga pro advogado que ele nao",
  "precisa de Git: ele precisa, pro app funcionar. O que NAO precisa de Git e esta copia de arquivos",
  "aqui, que voce faz com PowerShell. Se o Git faltar, oriente ele a instalar pelo site e siga copiando.",
  "",
  "1. Dentro deste ZIP ha uma pasta \".claude\" (comeca com ponto: o Windows a trata como OCULTA,",
  "   entao o advogado pode achar que o ZIP esta vazio. Ela esta la, confie e use os comandos acima).",
  "   Dentro dela ha uma pasta por skill (peticao-builder, calculo-previdenciario...) e a pasta \"commands\".",
  "2. Copie essas pastas para dentro da pasta .claude do usuario ($env:USERPROFILE\\.claude no Windows,",
  "   ~/.claude no Mac), juntando com o que ja existir. NAO altere settings.json, CLAUDE.md, permissoes",
  "   nem hooks existentes. Se houver arquivo de mesmo nome, pergunte antes de substituir.",
  "3. A instalacao e SO copia de arquivos: nada e executado durante a copia, e nao ha nenhum hook, cron ou tarefa que rode sozinha.",
  "4. Ao terminar, CONFIRME que deu certo antes de avisar o advogado: a pasta commands/maestria.md e a",
  "   pasta peticao-builder tem que existir dentro do .claude do usuario. Se nao existirem, diga que",
  "   falhou e peca pra ele chamar o suporte. NUNCA diga que instalou sem ter conferido.",
  "",
  "O QUE TEM DENTRO (transparencia total, pode conferir tudo):",
  "- Arquivos .md (comandos), modelos .docx e um licenca.json por skill (contem so o token da licenca, NAO o CPF).",
  "- Cerca de 68 scripts .py auxiliares, que o advogado usa DEPOIS, quando pede uma acao. A grande maioria (63) roda 100% local (gerar Word, ler PDF, calcular, transcrever audio com Whisper local). Poucos (3) fazem chamadas de rede A APIs JURIDICAS OFICIAIS, e SOMENTE quando o advogado usa essas funcoes, nunca sozinhos:",
  "   * juris_search.py, consultar_processo.py e jurimetria.py consultam o DataJud do CNJ (api-publica.datajud.cnj.jus.br), dados PUBLICOS do judiciario com token publico e gratuito do proprio CNJ, e sites de tribunais (TJs, TRFs) com jurisprudencia publica.",
  "   * juris_search.py pode chamar o Perplexity (api.perplexity.ai) SO se o advogado configurar a propria chave, para ajudar a encontrar julgados que sao DEPOIS validados na fonte oficial.",
  "",
  "Isso e a funcao ANTI-ALUCINACAO do produto: conferir cada jurisprudencia em fonte oficial em vez de inventar. O que vai pra rede e a CONSULTA JURIDICA que o advogado digita (tema, numero de processo publico, assunto do tribunal). As skills foram feitas pra NAO enviar os dados sensiveis do cliente (CPF, laudo, historico): ficam na maquina, e o advogado controla o que digita. A jurimetria nao usa nome de parte, juiz ou perito (LGPD). O token do DataJud e publico e compartilhado (do proprio CNJ), nao vinculado ao advogado.",
  "",
  "Voce pode abrir juris_search.py, consultar_processo.py e jurimetria.py (e qualquer outro) para confirmar. Nenhum script roda na instalacao nem por conta propria: so quando o advogado pede uma busca.",
  "",
  "A licenca ja foi validada quando a pessoa entrou na area de membros (maestria.samurailab.com.br/membros) com codigo + CPF/CNPJ. Para reinstalar ou gerenciar, o endereco e esse.",
  "",
  "ULTIMO PASSO (avise o advogado com estas palavras, e importante): pra as skills aparecerem, ele precisa REINICIAR o Claude Code por completo. FECHE o Claude Code inteiro (o aplicativo todo, nao so esta conversa), ABRA de novo, comece uma conversa NOVA e digite /maestria. So abrir conversa nova SEM fechar o app NAO funciona: os comandos so carregam quando o app reabre.",
  "",
].join("\n");

// Mapeia o plano do cliente pro bundle generico ja-instalado (sem licenca)
function bundleGenericoUrl(plano) {
  const full = ["full", "vitalicio", "black", "cortesia"];
  if (full.includes(plano)) return STORAGE_PUB + "maestria-full-generico.zip";
  const areas = (plano || "").replace("pacote_", "");
  const disp = ["prev", "trab", "marketing", "prev_trab"];
  return disp.includes(areas) ? STORAGE_PUB + "maestria-" + areas + "-generico.zip" : null;
}

// Baixa o bundle ja-instalado do plano e injeta o licenca.json de cada skill
// (com o token do cliente logado) + o LEIA. O Claude so precisa COPIAR pra ~/.claude:
// sem CPF, sem download remoto, sem instrucao oculta. A trava de 3 maquinas roda
// depois, no primeiro /maestria (check-in da skill, so token, sem CPF).
async function baixarInstaladorPersonalizado(botao, dados) {
  const cred = credenciais();
  const plano = (dados && dados.cliente) ? dados.cliente.plano : "";
  const skills = (dados && dados.skills) || [];
  const bundleUrl = bundleGenericoUrl(plano);
  const textoOriginal = botao.textContent;
  try {
    botao.textContent = "Preparando o seu instalador...";
    botao.disabled = true;
    if (!bundleUrl || !skills.length) throw new Error("sem-bundle");
    const resp = await fetch(bundleUrl + "?cb=" + Date.now());
    if (!resp.ok) throw new Error("download falhou");
    let bytes = new Uint8Array(await resp.arrayBuffer());
    const lic = new TextEncoder().encode(
      JSON.stringify({ token: cred.token, ativo: true, ativado_em: "area-de-membros" }, null, 2),
    );
    skills.forEach((s) => {
      if (s.skill_id) bytes = anexarAoZip(bytes, ".claude/" + s.skill_id + "/licenca.json", lic);
    });
    bytes = anexarAoZip(bytes, "LEIA-PRIMEIRO-MAESTRIA.txt", new TextEncoder().encode(LEIA_MAESTRIA));
    const blob = new Blob([bytes], { type: "application/zip" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "MaestrIA-Instalar.zip";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 30000);
    botao.textContent = "Baixado! Arrasta pro Claude e escreve: instala pra mim";
    setTimeout(() => { botao.textContent = textoOriginal; botao.disabled = false; }, 8000);
  } catch (e) {
    // Fallback: instalador de instrucoes (transparente), serve qualquer plano
    botao.textContent = textoOriginal;
    botao.disabled = false;
    window.location.href = URL_INSTALADOR;
  }
}

function renderizarDownloads(dados) {
  const grid = $("dl-skills");
  grid.innerHTML = "";

  // Card PASSO 0 (Windows): preparador de 1 clique que instala Git + Python via winget,
  // ANTES do Claude Code. Resolve o "Git é necessário para sessões locais" na raiz.
  // Mac não precisa (Git vem com o sistema, Python o Claude instala on-demand).
  const prep = document.createElement("div");
  prep.className = "card";
  prep.innerHTML =
    "<h3>⚙ Passo 0 (Windows): prepare seu computador</h3>" +
    "<p>No Windows, o Claude Code precisa do <strong>Git</strong> instalado (e as skills usam o <strong>Python</strong>). Este arquivo instala os dois sozinho, em 2 a 3 minutos, e sempre pega a versão mais nova. <strong>Rode ele ANTES de instalar o Claude Code.</strong></p>" +
    "<p class='mini'>Vai aparecer um aviso azul do Windows: clique em <strong>Mais informações &gt; Executar assim mesmo</strong>. E uma janela pedindo permissão de administrador: clique em <strong>Sim</strong>. As duas são normais.</p>" +
    "<a class='btn-baixar' href='/Preparar-meu-PC.bat' download>Baixar o preparador (Windows)</a>" +
    "<p class='mini' style='margin-top:8px;'>No <strong>Mac</strong> você não precisa disto: o Git já vem no sistema. Pule pro seu instalador abaixo.</p>";
  grid.appendChild(prep);

  // Card ÚNICO de download: um arquivo instala (e atualiza) o pacote inteiro.
  // Decisão 09/07: NUNCA listar zips individuais aqui, comprador leigo se confunde.
  // Desde 13/07 o botão gera o instalador PERSONALIZADO (licença embutida):
  // o Claude não pede código, só a confirmação do CPF/CNPJ.
  const inst = document.createElement("div");
  inst.className = "card";
  inst.style.borderColor = "var(--vermelho, #e33)";
  inst.innerHTML =
    "<h3>⬇ Seu pacote (um arquivo só)</h3>" +
    "<p>Este arquivo já vem com <strong>todas as suas skills e a sua licença dentro</strong>. Baixa, arrasta pra conversa do <strong>Claude Code</strong> e escreve <strong>instala pra mim</strong>: ele só copia pra você, sem digitar código nem CPF. Serve também pra ATUALIZAR: baixa e instala de novo por cima, nada do que você configurou se perde.</p>" +
    "<button type='button' class='btn-baixar' id='btn-instalador-perso'>Baixar meu instalador</button>" +
    "<p class='mini' style='margin-top:8px;'>Travou? <button type='button' class='link-aula' data-abrir-aula='01-instalacao'>A aula de instalação te destrava</button>, aqui mesmo.</p>";
  grid.appendChild(inst);
  inst.querySelector("#btn-instalador-perso").addEventListener("click", function () {
    baixarInstaladorPersonalizado(this, dados);
  });

  // Lista informativa do que vem dentro (SEM botão de download, só transparência)
  const skills = dados.skills || [];
  if (skills.length) {
    const box = document.createElement("div");
    box.className = "card";
    let itens = "";
    skills.forEach((s) => {
      itens +=
        "<li><strong>" + esc(s.nome) + "</strong>" +
        " <span class='mini'>(versão " + esc(s.versao_atual) + ")</span></li>";
    });
    box.innerHTML =
      "<h3>O que vem no seu pacote</h3>" +
      "<p class='mini'>Tudo isso entra junto no instalador acima. Instalou, tá tudo dentro.</p>" +
      "<ul style='margin:8px 0 0 18px; line-height:1.7;'>" + itens + "</ul>";
    grid.appendChild(box);
  }

  const bloqueadas = dados.skills_bloqueadas || [];
  const upsell = $("dl-upsell");
  if (!bloqueadas.length) {
    upsell.classList.add("hidden");
    return;
  }
  upsell.classList.remove("hidden");
  const gridB = $("dl-bloqueadas");
  gridB.innerHTML = "";
  bloqueadas.forEach((s) => {
    const card = document.createElement("div");
    card.className = "card card-bloqueada";
    card.innerHTML =
      "<h3>🔒 " + esc(s.nome) + "</h3>" +
      "<p>" + esc((s.descricao || "").split(".")[0]) + ".</p>";
    gridB.appendChild(card);
  });
}

// ---------- Guia das skills (o que cada função faz, só as do pacote) ----------
function renderizarGuia(dados) {
  const box = $("guia-skills-lista");
  if (!box) return;
  box.innerHTML = "";
  const guia = window.MAESTRIA_GUIA || {};
  const skills = dados.skills || [];
  if (!skills.length) {
    box.innerHTML = "<p class='vazio'>Nenhuma skill liberada ainda.</p>";
    return;
  }

  // como usar (sempre no topo)
  const intro = document.createElement("div");
  intro.className = "card";
  intro.innerHTML =
    "<h3>Como usar qualquer função</h3>" +
    "<ol style='margin:10px 0 0 18px; line-height:1.8;'>" +
    "<li>Abra o <strong>Claude Code</strong> no seu computador.</li>" +
    "<li>Digite o comando da função (ex: <code>/maestria:nova-peticao</code>) e aperte Enter. Ou digite só <code>/maestria</code> pra ver o menu geral e escolher por lá.</li>" +
    "<li>A skill conduz o resto com perguntas, uma de cada vez. Pode responder em português normal e mandar documentos, prints e até áudio do cliente.</li>" +
    "<li>O resultado sai em <strong>Word</strong>, salvo na pasta que você escolheu, pronto pra abrir com dois cliques.</li>" +
    "</ol>" +
    "<p class='mini' style='margin-top:8px;'>Não precisa decorar nada: escrever o que você quer em português na central <code>/maestria</code> também funciona. Os comandos existem pra quem gosta de atalho.</p>";
  box.appendChild(intro);

  const liFunc = (comando, texto) =>
    "<li style='margin-bottom:10px;'><code>" + esc(comando) + "</code>" +
    "<div class='mini' style='margin:2px 0 0 2px; line-height:1.55;'>" + esc(texto) + "</div></li>";

  skills.forEach((s, i) => {
    const info = guia[s.skill_id];
    const det = document.createElement("details");
    det.className = "card";
    if (i === 0) det.open = true;
    let corpo = "";
    if (info && info.funcoes && info.funcoes.length) {
      corpo = "<ul style='margin:12px 0 0 18px; list-style:none; padding-left:0;'>";
      info.funcoes.forEach((f) => {
        corpo += liFunc("/maestria:" + f.c, f.d);
      });
      corpo += "</ul>";
    } else {
      corpo = "<p class='mini' style='margin-top:8px;'>" + esc(s.descricao || "") + "</p>";
    }
    det.innerHTML =
      "<summary style='cursor:pointer; font-weight:700; font-size:1.05em;'>" +
      esc(s.nome) +
      " <span class='mini'>(" + ((info && info.funcoes) ? info.funcoes.length + (info.funcoes.length === 1 ? " função própria" : " funções próprias") : "resumo") + ")</span></summary>" +
      "<p class='mini' style='margin-top:6px;'>" + esc((s.descricao || "").split(".")[0]) + ". Além das funções abaixo, esta skill tem todas as ferramentas dos blocos no fim da página.</p>" +
      corpo;
    box.appendChild(det);
  });

  // bloco fixo 1: ferramentas presentes em TODA skill
  const fixo = document.createElement("div");
  fixo.className = "card";
  fixo.innerHTML =
    "<h3>Em toda skill (peça pela central /maestria)</h3>" +
    "<p class='mini' style='margin-top:4px;'>Estas ferramentas existem em todas as skills. Digite <code>/maestria</code> e peça em português (ex: \"quero abrir um chamado\", \"onde ficam meus arquivos?\").</p>" +
    "<ul style='margin:12px 0 0 18px; list-style:none; padding-left:0;'>" +
    liFunc("menu", "Cardápio da skill em cards clicáveis, pra escolher o que fazer sem decorar comando.") +
    liFunc("setup rápido", "Configuração inicial guiada (uns 30 minutos): dados do escritório, tom de voz e preferências. Roda uma vez só.") +
    liFunc("configurar pastas", "Escolhe onde os documentos gerados ficam salvos: pasta do computador ou pasta do Google Drive sincronizado.") +
    liFunc("editar estilo", "Define palavras e construções que a MaestrIA nunca deve usar nos seus textos. Ela escreve do SEU jeito.") +
    liFunc("listar casos", "Mostra tudo o que você já gerou com a skill, organizado por caso.") +
    liFunc("abrir", "Abre o arquivo ou a pasta gerada direto no Explorer, sem caçar caminho.") +
    liFunc("economia", "Calcula quanto tempo e dinheiro a skill já te economizou, com base no seu valor por hora.") +
    liFunc("atualizar skill", "Puxa as correções e melhorias mais novas. A skill também avisa sozinha quando tem novidade.") +
    liFunc("suporte", "Abre um chamado direto pra gente. A resposta aparece aqui na sua área de membros.") +
    liFunc("ativar licença / minha licença", "Ativação da skill com o código da compra e consulta de validade.") +
    "</ul>";
  box.appendChild(fixo);

  // bloco fixo 2: inteligencia juridica compartilhada
  const intel = document.createElement("div");
  intel.className = "card";
  intel.innerHTML =
    "<h3>Inteligência jurídica (também em toda skill)</h3>" +
    "<ul style='margin:12px 0 0 18px; list-style:none; padding-left:0;'>" +
    liFunc("mesa", "Convoca TODOS os Conselheiros de uma vez pra debater seu caso ou sua peça. Cada um dá a opinião pela sua escola de pensamento e você vê o debate.") +
    liFunc("conselheiro", "Consulta UM Conselheiro por vez, pra uma análise profunda de um ângulo específico do caso.") +
    liFunc("consultar juízo", "Mostra a tendência decisória de um juízo específico num tema, com base no Banco Vivo de Decisões da MaestrIA.") +
    liFunc("contribuir decisão", "Doa uma decisão favorável sua (com os nomes das partes removidos automaticamente) pro Banco Vivo. Quanto mais advogados contribuem, mais forte o radar de todos.") +
    liFunc("ver insights", "Teses vencedoras, jurisprudência confirmada em fonte oficial e armadilhas conhecidas da sua área.") +
    "</ul>";
  box.appendChild(intel);
}

// ---------- Licença ----------
function renderizarLicenca(dados) {
  const c = dados.cliente;
  $("lic-situacao").textContent = c.vitalicio
    ? "Licença vitalícia, sem vencimento."
    : c.expirou
      ? "Licença vencida. Renove pra continuar usando."
      : "Licença ativa. Vence em " + dataBr(c.vence_em) + ".";
  $("lic-email").textContent = "Email da compra: " + (c.email || "");

  const maquinas = dados.instalacoes || [];
  $("lic-maquinas-contagem").textContent =
    "(" + maquinas.length + " de " + (dados.limite_dispositivos || 3) + ")";
  const ul = $("lic-maquinas");
  ul.innerHTML = "";
  if (maquinas.length === 0) {
    ul.innerHTML = "<li>Nenhum computador ativado ainda. Baixe seu instalador em Downloads e abra o /maestria uma vez.</li>";
  } else {
    maquinas.forEach((m) => {
      const li = document.createElement("li");
      const label = document.createElement("span");
      label.textContent = m.hostname + (m.os_info ? " (" + m.os_info + ")" : "") + " desde " + dataBr(m.ativada_em);
      li.appendChild(label);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "link-aula";
      btn.style.marginLeft = "10px";
      btn.textContent = "remover";
      btn.addEventListener("click", function () { removerDispositivo(m.hostname, btn); });
      li.appendChild(btn);
      ul.appendChild(li);
    });
  }
  const nota = $("lic-maquinas-nota");
  if (nota) {
    nota.textContent = "Trocou de computador? Remova o antigo aqui pra liberar a vaga. Precisa de mais de " +
      (dados.limite_dispositivos || 3) + " máquinas? Fale com o suporte que a gente libera.";
  }
}

// Remove um dispositivo da licença (libera uma vaga das 3). Exige token + CPF (login).
async function removerDispositivo(hostname, botao) {
  if (!window.confirm('Remover "' + hostname + '"? Isso libera uma vaga; você poderá instalar em outra máquina.')) return;
  const cred = credenciais();
  if (!cred) return;
  botao.disabled = true;
  botao.textContent = "removendo...";
  try {
    const resp = await fetch(CORE + "/remove-device", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: cred.token, cpf: cred.cpf, hostname: hostname }),
    });
    const d = await resp.json();
    if (!resp.ok || !d.ok) throw new Error(d.erro || "erro");
    await entrar(cred.token, cred.cpf, false); // recarrega a área e atualiza a lista
  } catch (e) {
    botao.disabled = false;
    botao.textContent = "remover";
    window.alert("Não deu pra remover agora. Tente de novo em instantes.");
  }
}

// ---------- Chamados ----------
function renderizarTickets(tickets) {
  const box = $("pl-tickets");
  box.innerHTML = "";
  if (!tickets.length) {
    box.innerHTML = "<p class='vazio'>Você ainda não abriu nenhum chamado.</p>";
    return;
  }
  tickets.forEach((t) => {
    const respondido = Boolean(t.resposta);
    const el = document.createElement("div");
    el.className = "ticket";
    el.innerHTML =
      "<div class='ticket-head'>" +
      "<strong>#" + esc(t.numero) + " · " + esc(t.resumo) + "</strong>" +
      "<span class='ticket-status " + (respondido ? "respondido" : "aberto") + "'>" +
      (respondido ? "Respondido" : "Em análise") + "</span></div>" +
      "<p class='meta'>" + esc(t.skill_id) + " · aberto em " + dataBr(t.created_at) + "</p>" +
      (respondido
        ? "<div class='resposta'><strong>Resposta" +
          (t.respondido_em ? " em " + dataBr(t.respondido_em) : "") +
          "</strong><br>" + esc(t.resposta) + "</div>"
        : "");
    box.appendChild(el);
  });
}

function montarSelectChamado(dados) {
  const sel = $("tk-skill");
  sel.innerHTML = "";
  (dados.skills || []).forEach((s) => {
    const opt = document.createElement("option");
    opt.value = s.skill_id;
    opt.textContent = s.nome;
    sel.appendChild(opt);
  });
  const optOutra = document.createElement("option");
  optOutra.value = "outra";
  optOutra.textContent = "Outra / assunto geral";
  sel.appendChild(optOutra);
}

// ---------- novo chamado ----------
$("form-ticket").addEventListener("submit", async (e) => {
  e.preventDefault();
  const cred = credenciais();
  if (!cred) return;

  const msg = $("ticket-msg");
  msg.className = "hidden";
  const btn = e.target.querySelector("button[type=submit]");
  btn.disabled = true;
  btn.textContent = "Enviando...";

  try {
    const resp = await fetch(CORE + "/skill-support-ticket", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skill_id: $("tk-skill").value,
        cliente_token: cred.token,
        email_contato: dadosAtuais && dadosAtuais.cliente ? dadosAtuais.cliente.email : "",
        categoria: $("tk-categoria").value,
        severidade: "medio",
        resumo: $("tk-resumo").value.trim(),
        descricao: $("tk-descricao").value.trim(),
        versao_skill: null,
        os: navigator.userAgent.includes("Mac") ? "mac" : "windows",
      }),
    });
    const dados = await resp.json();
    if (!resp.ok || !dados.ok) throw new Error("Não deu pra enviar. Tente de novo em instantes.");

    msg.textContent = "Chamado #" + dados.numero + " aberto! A resposta aparece aqui e chega no seu email em até 48h úteis.";
    msg.className = "ok";
    e.target.reset();

    // Recarrega os chamados
    await entrar(cred.token, cred.cpf, false);
    mostrarView("chamados");
  } catch (err) {
    msg.textContent = err.message || "Falha de conexão. Tente de novo.";
    msg.className = "falha";
  } finally {
    btn.disabled = false;
    btn.textContent = "Enviar chamado";
  }
});

// ---------- sessão persistida ----------
(async function init() {
  const cred = credenciais();
  if (cred && cred.token) {
    await entrar(cred.token, cred.cpf, false);
  }
})();
