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

  // ⛔ Quem ainda NAO instalou ve um caminho so. O mural de seis cards e o que
  // trava a pessoa que acabou de comprar: ela precisa de uma coisa de cada vez.
  // A prova de instalacao e a maquina registrada, a mesma que a aba de licenca
  // mostra. Se a deteccao falhar, o pior caso e ver a tela antiga.
  const jaInstalou = ((dados && dados.instalacoes) || []).length > 0;
  const pp = $("ini-primeiros-passos");
  const grade = document.querySelector(".grid-acoes");
  const progresso = document.querySelector(".progresso-wrap");
  if (pp) {
    const mostrarPasso = !jaInstalou && !localStorage.getItem("maestria_pulou_passos");
    pp.classList.toggle("hidden", !mostrarPasso);
    if (grade) grade.classList.toggle("hidden", mostrarPasso);
    if (progresso) progresso.classList.toggle("hidden", mostrarPasso);
    // ⛔ o banner "Bem-vindo" come 144px antes do bloco e nao diz nada a quem
    // acabou de chegar. Com ele na tela, o passo 3 (baixar e instalar) cai para
    // fora do campo de visao, e quem esta travado nao rola: faz o que esta la.
    const hero = document.querySelector("#view-inicio .inicio-hero");
    if (hero) hero.classList.toggle("hidden", mostrarPasso);
    // ⛔ o botao do curso vive FORA da .progresso-wrap: esconder so a barra
    // deixava um "Comecar: ..." solto por cima do passo 1.
    const btnCurso = $("ini-continuar");
    if (btnCurso) btnCurso.classList.toggle("hidden", mostrarPasso);
    const liberar = () => {
      const p3 = $("pp-passo3");
      if (p3) p3.classList.add("pp-liberado");
    };
    const jaTenho = $("pp-ja-tenho");
    if (jaTenho) jaTenho.onclick = liberar;
    // quem vai ver a aula tambem destrava o passo 3 para quando voltar
    pp.querySelectorAll("[data-abrir-aula]").forEach((b) => b.addEventListener("click", liberar));
    const pular = $("pp-ja-instalei");
    if (pular) {
      pular.onclick = () => {
        localStorage.setItem("maestria_pulou_passos", "1");
        pp.classList.add("hidden");
        if (grade) grade.classList.remove("hidden");
        if (progresso) progresso.classList.remove("hidden");
        if (hero) hero.classList.remove("hidden");
        if (btnCurso) btnCurso.classList.remove("hidden");
      };
    }
  }

  // ⛔ Antes de montar qualquer coisa do curso: o curso precisa saber o pacote
  // dele para esconder as aulas e os trechos de area que ele nao comprou.
  if (window.MAESTRIA_CURSO && window.MAESTRIA_CURSO.definirAreas) {
    window.MAESTRIA_CURSO.definirAreas(dados && dados.cliente ? dados.cliente.plano : "");
  }

  montarUpgrade(dados, jaInstalou);

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

// ---------- Áreas do direito: nome de gente para o código ----------
// Usado pela aba Downloads e pela aba Guia. Uma cópia só, de propósito: duas
// listas iguais em lugares diferentes é uma delas ficando velha sem ninguém ver.
const NOME_AREA = {
  prev: "Previdenciário", trab: "Trabalhista", marketing: "Marketing jurídico",
  familia: "Família", consumidor: "Consumidor", criminal: "Criminal",
  saude: "Saúde", tributario: "Tributário", imob: "Imobiliário",
  empresarial: "Empresarial", universal: "Serve para qualquer área",
};
function rotuloArea(a) {
  return NOME_AREA[a] || (a ? a.charAt(0).toUpperCase() + a.slice(1) : "Outras");
}
// "Serve para qualquer área" vai por último: é apoio, não é área de ninguém.
function pesoArea(a) { return a === "universal" ? 2 : 1; }
function agruparPorArea(lista) {
  const mapa = new Map();
  (lista || []).forEach((s) => {
    const a = s.area || "outras";
    if (!mapa.has(a)) mapa.set(a, []);
    mapa.get(a).push(s);
  });
  return new Map(Array.from(mapa.entries()).sort(
    (x, y) => pesoArea(x[0]) - pesoArea(y[0]) || rotuloArea(x[0]).localeCompare(rotuloArea(y[0]), "pt-BR")));
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

// Instruções de instalação com conferência do ambiente e preservação.
const LEIA_MAESTRIA = [
  "MaestrIA | Instalação no Claude Code",
  "",
  "Este pacote contém os arquivos do produto e a licença pessoal de quem o baixou. Não publique o ZIP nem mostre o conteúdo de licenca.json na conversa.",
  "",
  "COMO CONDUZIR",
  "Fale em português do Brasil, com frases curtas e respeito. Faça uma etapa por vez. Execute o que estiver autorizado e ao seu alcance. Se precisar do advogado, peça apenas a ação que falta. Não prometa prazo antes de conferir o ambiente. Nunca diga que instalou quando apenas explicou como instalar.",
  "",
  "1. CONFIRA O AMBIENTE ANTES DE PROMETER",
  "Verifique se tem ferramentas para ler este ZIP, executar operações locais e escrever na configuração do Claude deste usuário. Confirme o sistema operacional e a pasta de trabalho existente.",
  "Se estiver em chat comum, ambiente de nuvem ou sem acesso local, não tente contornar permissões. Explique: \"Abra o aplicativo Claude, entre em Code, escolha Este computador e uma pasta sua. Anexe este mesmo ZIP naquela conversa e escreva instala pra mim.\" Mostre https://maestria.samurailab.com.br/instalacao.html#code. Pare apenas a instalação dependente desse acesso.",
  "Se a pasta selecionada não existe mais, oriente a selecionar uma pasta existente. A pasta de documentos pode se chamar MaestrIA-Arquivos, dentro da pasta pessoal, fora do OneDrive. Não peça para escolher .claude como pasta dos casos.",
  "\"Não é um repositório Git\" não é o mesmo erro que \"Git é necessário para sessões locais\". Não crie repositório nem apague conversas para resolver um endereço de pasta inválido.",
  "",
  "2. EXPLIQUE O QUE VAI ACONTECER",
  "Diga: \"Vou conferir o pacote e copiar a MaestrIA para o Claude. Vou preservar suas configurações e guardar uma cópia dos arquivos que precisarem ser atualizados. A instalação também registra sua licença e o nome deste computador no MaestrIA e acrescenta regras de conferência de fontes às conversas. No fim vamos abrir a central para conferir.\"",
  "Não esconda esses efeitos. Leia e respeite as permissões do aplicativo. Não desative proteções, não altere o modo de permissões e não peça para ignorar alertas de segurança.",
  "",
  "3. COPIE COM PRESERVAÇÃO E CÓPIA DE SEGURANÇA",
  "O ZIP tem uma pasta .claude. Inspecione a lista completa antes de extrair: recuse caminhos absolutos, caminhos que escapem da pasta de extração, links simbólicos e entradas duplicadas. Extraia em uma pasta temporária exclusiva desta execução. Não use uma pasta temporária compartilhada com instalação anterior.",
  "O destino normal é a pasta .claude dentro da pasta pessoal do usuário. No Windows, use operações nativas do PowerShell. A extração não precisa de Python ou Git. No Mac, use as ferramentas locais disponíveis. Não execute scripts de dentro do pacote apenas para copiar arquivos.",
  "Antes de qualquer substituição, guarde cópia dos arquivos existentes em uma pasta de backup com data fora do destino e registre os caminhos alterados. Não apague arquivos que não pertencem ao pacote. Não use cópia recursiva forçada indiscriminada sobre a configuração inteira.",
  "Preserve sempre settings.json, settings.local.json, hooks, conectores, memórias, projetos, marca, tom de voz, preferências e pastas configuradas. Dentro das skills preserve os arquivos pessoais de configuração já existentes. Se houver conflito que você não consiga distinguir de personalização do advogado, pare apenas esse arquivo e explique a escolha necessária. Atualize os comandos e arquivos do produto identificados como pertencentes ao pacote.",
  "Não substitua uma licença existente de outra pessoa silenciosamente. Não imprima tokens. O CPF não faz parte deste ZIP e não é necessário para a cópia. Se faltar licença válida no pacote, não fabrique uma: oriente a baixar novamente em Downloads da área de membros.",
  "",
  "4. CONFIRA OS ARQUIVOS E OS PROGRAMAS",
  "Compare os arquivos copiados com os arquivos do ZIP por hash, exceto configurações pessoais preservadas e identificadas no relatório. Confirme commands/maestria.md, as pastas de TODAS as skills licenciadas do pacote, seus comandos e licenca.json. Não exija uma skill de outra área. Marketing sozinho não precisa de peticao-builder.",
  "Registre as versões encontradas em versao.json e as pendências. Uma conferência de existência isolada não comprova que a atualização inteira terminou.",
  "Confira Git e Python executando a consulta de versão dos programas disponíveis. No Windows, um atalho python que abre a Microsoft Store não é Python instalado. Se faltar apoio, explique o item que falta e indique https://maestria.samurailab.com.br/instalacao.html#preparar. Instale apenas quando autorizado e use fontes oficiais. Se a máquina do escritório bloquear, não contorne a política: o responsável pela máquina ou o grupo deve ajudar.",
  "Não instale o motor de vídeo durante a cópia do pacote. A preparação do editor é uma etapa própria, solicitada pelo comando /maestria:preparar-editor, que informa os downloads e confere a versão do motor.",
  "",
  "5. REGISTRE A INSTALAÇÃO COM TRANSPARÊNCIA",
  "Após conferir a cópia, leia o campo token de um licenca.json instalado sem exibi-lo. Faça POST JSON para https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1/device-checkin com token, hostname (nome real desta máquina), os_info (windows ou mac) e skill_version \"instalacao\". Não envie documentos, CPF nem o conteúdo dos casos.",
  "Se a API rejeitar licença ou limite de dispositivos, explique a pendência. A área de membros, aba Licença, permite consultar as vagas e gerenciar os computadores. Não afirme um limite fixo: ele depende da licença.",
  "Se a rede falhar, informe \"Arquivos copiados; registro da instalação pendente de conexão\". Não chame isso de ativação concluída e não esconda o erro. Não repita indefinidamente.",
  "",
  "6. ACRESCENTE AS REGRAS SEM APAGAR TEXTO DO USUÁRIO",
  "Grave maestria-regras.md dentro da .claude com estas orientações:",
  "- Confira número e conteúdo de jurisprudência na fonte oficial antes de citar. Se não conferiu, diga isso.",
  "- Confira a fonte de leis e normas antes de afirmar seu conteúdo.",
  "- Separe fatos verificados, hipóteses e critérios ao comparar cálculos ou ferramentas.",
  "- Preserve versões e cenários de cálculos em andamento.",
  "- Aponte riscos profissionais e a fonte aplicável; o advogado decide e revisa o resultado.",
  "- Escreva em português do Brasil, com acentuação correta.",
  "No CLAUDE.md do usuário, acrescente ao fim, sem reescrever o texto existente:",
  "<!-- MAESTRIA:INICIO (gerado pela MaestrIA; pode remover este bloco quando quiser) -->",
  "@maestria-regras.md",
  "<!-- MAESTRIA:FIM -->",
  "Se já houver um bloco MAESTRIA, preserve as regras existentes e não duplique o bloco. Se o arquivo de regras já existir, preserve-o nesta instalação. Antes de alterar, faça backup. Se não puder gravar, informe a pendência. Essas regras são lidas também fora dos comandos MaestrIA; não oculte esse alcance.",
  "",
  "7. CONFIRA A CENTRAL COM O ADVOGADO",
  "Depois da cópia e das verificações, diga o que foi instalado, o que foi preservado, onde está o backup e se há alguma pendência. Não exponha a licença.",
  "Peça para abrir uma nova conversa local e enviar /maestria. Se o comando não aparecer, peça para fechar o aplicativo inteiro e abrir novamente. Não afirme que toda versão exige reiniciar sempre.",
  "A instalação só está conferida de ponta a ponta quando a central abrir e uma ferramenta do pacote produzir um resultado que o advogado consegue abrir. Use dados fictícios no primeiro exemplo. Não diga que um documento está correto sem revisão.",
  "Para quem já instalou e quer atualizar, o caminho normal é /maestria:atualizar-skill. Reinstalar e atualizar não são a mesma operação. Preserve configurações em ambos.",
  "",
  "AJUDA E PRIVACIDADE",
  "Se não resolver com a correção simples correspondente ao erro, peça um print com a etapa e a mensagem, sem licença ou dados de clientes, no grupo da comunidade MaestrIA: https://chat.whatsapp.com/KQcIy0D6Tp5IWtWY2WXRx7. Não invente chamados, e-mail de suporte nem prazo de resposta.",
  "Os arquivos de trabalho ficam na pasta escolhida, mas o Claude usa serviços da Anthropic conforme a conta e suas políticas. Não prometa que todo conteúdo processado pela IA fica exclusivamente no computador. Recursos opcionais podem usar serviços externos e devem explicar os dados e custos antes do uso.",
  "Guia visual: https://maestria.samurailab.com.br/instalacao.html",
  "",
].join("\n");

// Mapeia o plano do cliente pro bundle generico ja-instalado (sem licenca).
// Devolve uma LISTA de candidatos, do mais especifico pro mais abrangente.
//
// FURO QUE ISSO CORRIGE (23/07): a versao antiga so aceitava uma lista fixa
// (prev, trab, marketing, prev_trab). O cliente de `pacote_prev_marketing`
// caia fora dela, a funcao devolvia null e o download NUNCA funcionava, em
// maquina nenhuma, com uma mensagem falsa de "conexao instavel". Agora qualquer
// combinacao de areas e montada dinamicamente e, se faltar o arquivo, o full
// (que contem tudo) segura: a licenca so e injetada nas skills do plano, entao
// o cliente nunca fica travado por causa de uma combinacao nova de pacote.
function bundlesCandidatos(plano, temAntecipada) {
  const full = ["full", "vitalicio", "black", "cortesia"];
  const urlDe = (n) => STORAGE_PUB + "maestria-" + n + "-generico.zip";
  // Cliente de piloto (skills liberadas antes do lancamento): usa o pacote que
  // TEM essas skills dentro. Sem isso o instalador traria so as do plano e
  // criaria pasta orfa, com licenca e sem skill. Cai pro full se faltar.
  if (temAntecipada) return [urlDe("full-piloto"), urlDe("full")];
  if (full.includes(plano)) return [urlDe("full")];
  const areas = (plano || "").replace("pacote_", "");
  if (!areas) return [urlDe("full")];
  const partes = areas.split("_").filter(Boolean);
  const cand = [areas];                                  // ordem exata do plano
  if (partes.length > 1) cand.push(partes.slice().reverse().join("_"));  // ordem inversa
  cand.push("full");                                     // rede de seguranca
  return cand.map(urlDe);
}

// Baixa o pacote com timeout + 1 retry, pra um soluco de rede numa maquina
// travada nao derrubar tudo (foi o que travou o Jean na 2a maquina dele).
async function fetchPacote(url, tentativas) {
  let ultimoErro;
  for (let i = 0; i < tentativas; i++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 45000);
    try {
      const sep = url.includes("?") ? "&" : "?";
      const resp = await fetch(url + sep + "cb=" + Date.now(), { signal: ctrl.signal });
      clearTimeout(timer);
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      return new Uint8Array(await resp.arrayBuffer());
    } catch (e) {
      clearTimeout(timer);
      ultimoErro = e;
    }
  }
  throw ultimoErro || new Error("download falhou");
}

// Tenta os candidatos em ordem: se o bundle da combinacao exata nao existir no
// Storage (404), cai pro proximo, e no fim pro full. So desiste se TODOS
// falharem, e ai o erro e de verdade (rede), nao de plano sem arquivo.
async function fetchPrimeiroDisponivel(urls) {
  let ultimoErro;
  for (const url of urls) {
    try {
      return await fetchPacote(url, 2);
    } catch (e) {
      ultimoErro = e;
    }
  }
  throw ultimoErro || new Error("nenhum bundle disponivel");
}

// Baixa o bundle ja-instalado do plano e injeta o licenca.json de cada skill
// (com o token do cliente logado) + o LEIA. O Claude so precisa COPIAR pra ~/.claude:
// sem CPF, sem download remoto, sem instrucao oculta. A trava de 3 maquinas roda
// depois, no primeiro /maestria (check-in da skill, so token, sem CPF).
//
// IMPORTANTE (instalar em outra maquina TEM que funcionar): alem de tentar o
// download automatico, mostramos SEMPRE um link real e visivel. Maquina travada
// (antivirus, politica de empresa, navegador restrito) bloqueia o clique
// automatico SEM dar erro; o clique do proprio usuario no link nao e bloqueado.
async function baixarInstaladorPersonalizado(botao, dados) {
  const cred = credenciais();
  const plano = (dados && dados.cliente) ? dados.cliente.plano : "";
  const skills = (dados && dados.skills) || [];
  const temAntecipada = skills.some((s) => s && s.acesso_antecipado);
  const candidatos = bundlesCandidatos(plano, temAntecipada);
  const textoOriginal = botao.textContent;
  const ajuda = $("dl-perso-ajuda");
  if (ajuda) ajuda.innerHTML = "";
  try {
    botao.textContent = "Preparando o seu instalador...";
    botao.disabled = true;
    if (!skills.length) throw new Error("sem-skills");
    let bytes = await fetchPrimeiroDisponivel(candidatos);
    const lic = new TextEncoder().encode(
      JSON.stringify({ token: cred.token, ativo: true, ativado_em: "area-de-membros" }, null, 2),
    );
    skills.forEach((s) => {
      if (s.skill_id) bytes = anexarAoZip(bytes, ".claude/" + s.skill_id + "/licenca.json", lic);
    });
    bytes = anexarAoZip(bytes, "LEIA-PRIMEIRO-MAESTRIA.txt", new TextEncoder().encode(LEIA_MAESTRIA));
    const blob = new Blob([bytes], { type: "application/zip" });
    const blobUrl = URL.createObjectURL(blob);

    // Link real e visivel: a rede de seguranca contra download automatico bloqueado.
    if (ajuda) {
      ajuda.innerHTML =
        "<a class='btn-baixar' id='dl-perso-link' href='" + blobUrl + "' download='MaestrIA-Instalar.zip'>" +
        "⬇ Clique aqui pra salvar o seu instalador</a>" +
        "<p class='mini' style='margin-top:6px;'>Se o download não começou sozinho, use este botão. " +
        "Abra o aplicativo Claude, entre em <strong>Code → Este computador</strong>, escolha sua pasta e anexe <strong>MaestrIA-Instalar.zip</strong>. Depois " +
        "escreve <strong>instala pra mim</strong>.</p>";
    }
    // Tenta tambem o automatico (funciona na maioria das maquinas).
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = "MaestrIA-Instalar.zip";
    document.body.appendChild(a);
    a.click();
    a.remove();
    // 10 minutos: tempo de sobra pro usuario achar/clicar o link manual acima.
    setTimeout(() => URL.revokeObjectURL(blobUrl), 600000);
    botao.textContent = "Instalador pronto ✓";
    setTimeout(() => { botao.textContent = textoOriginal; botao.disabled = false; }, 8000);
  } catch (e) {
    // Plano B honesto: NAO joga o usuario pra fora nem entrega instalador sem
    // licenca (que faria o Claude pedir o codigo). Fica na pagina e oferece
    // tentar de novo: quase sempre e conexao instavel e resolve na 2a.
    botao.textContent = textoOriginal;
    botao.disabled = false;
    if (ajuda) {
      // Mensagem HONESTA por causa: culpar a conexão quando o problema é o
      // cadastro faz o advogado tentar de novo pra sempre, sem sair do lugar.
      const semSkills = String(e && e.message) === "sem-skills";
      ajuda.innerHTML = semSkills
        ? "<p class='mini' style='color:var(--vermelho,#e33);'>Não achamos nenhuma skill liberada " +
          "nesta licença, então não dá pra montar o instalador. Isso é com a gente, não com você: " +
          "mande um print no grupo da comunidade, sem mostrar sua licença.</p>"
        : "<p class='mini' style='color:var(--vermelho,#e33);'>Não foi possível baixar ou montar o pacote e não deu " +
          "para concluir o download agora. Tente novamente. Se continuar, mande um print no grupo.</p>" +
          "<button type='button' class='btn-baixar' id='dl-perso-retry'>Tentar de novo</button>";
      const rb = $("dl-perso-retry");
      if (rb) rb.addEventListener("click", function () { baixarInstaladorPersonalizado(botao, dados); });
    }
  }
}

function renderizarDownloads(dados) {
  const grid = $("dl-skills");
  grid.innerHTML = "";

  // O guia fica antes dos downloads para orientar ambiente e pasta.
  const prep = document.createElement("div");
  prep.className = "card";
  prep.innerHTML =
    "<h3>1. Veja onde clicar antes de instalar</h3>" +
    "<p>Abra o aplicativo Claude, entre em <strong>Code</strong>, escolha <strong>Este computador</strong> e uma pasta sua. O vídeo mostra cada controle.</p>" +
    "<button type='button' class='btn-baixar link-aula' data-abrir-aula='01-instalacao'>Assistir à instalação, tela a tela</button>" +
    "<h3>2. Confira os programas de apoio</h3>" +
    "<p>No Windows, o preparador confere e instala Git e Python quando faltam. Leia o resultado antes de continuar. O tempo depende do computador e da conexão.</p>" +
    "<a class='btn-baixar' href='/Preparar-meu-PC.bat' download>Baixar o preparador do Windows</a>" +
    "<p class='mini'>Se o Windows bloquear, confira a origem e peça ajuda no grupo ou ao responsável pelo computador. Não desative as proteções. No Mac, siga a orientação específica do guia, sem executar este arquivo.</p>";
  grid.appendChild(prep);

  // Card ÚNICO de download: um arquivo instala (e atualiza) o pacote inteiro.
  // Decisão 09/07: NUNCA listar zips individuais aqui, comprador leigo se confunde.
  // Desde 13/07 o botão gera o instalador PERSONALIZADO (licença embutida):
  // o Claude não pede código, só a confirmação do CPF/CNPJ.
  const inst = document.createElement("div");
  inst.className = "card";
  inst.style.borderColor = "var(--vermelho, #e33)";
  inst.innerHTML =
    "<h3>3. Baixe seu pacote e peça a instalação</h3>" +
    "<p>Este arquivo já vem com <strong>todas as suas skills e a sua licença dentro</strong>. Na sessão local de <strong>Code → Este computador</strong>, anexe o ZIP e escreva <strong>instala pra mim</strong>. A instalação confere o ambiente e preserva suas configurações. Depois, abra <strong>/maestria</strong> para conferir. Já instalou? Atualize com <strong>/maestria:atualizar-skill</strong>.</p>" +
    "<button type='button' class='btn-baixar' id='btn-instalador-perso'>Baixar meu instalador</button>" +
    "<div id='dl-perso-ajuda' style='margin-top:10px;'></div>" +
    "<p class='mini' style='margin-top:8px;'>Vai usar em <strong>outra máquina</strong>? É só entrar nesta área de membros no outro computador e baixar de novo, funciona igual. Chegou no limite de máquinas? Você mesmo libera uma na aba <strong>Licença</strong>, na hora.</p>" +
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
    let qtdAntecipadas = 0;
    const porArea = agruparPorArea(skills);
    let itens = "";
    porArea.forEach((lista, area) => {
      itens += "<li style='list-style:none; margin:14px 0 6px -18px; font-weight:700;'>" +
        esc(rotuloArea(area)) + " <span class='mini' style='font-weight:400'>(" + lista.length +
        (lista.length === 1 ? " skill" : " skills") + ")</span></li>";
      lista.forEach((s) => {
        // Skill liberada antes do lancamento (piloto): marca na lista, senao a
        // pessoa ve um nome que nao reconhece e nao sabe o que fazer com ele.
        const selo = s.acesso_antecipado
          ? " <span class='mini' style='color:#c9a227'>· acesso antecipado</span>"
          : "";
        if (s.acesso_antecipado) qtdAntecipadas++;
        itens +=
          "<li><strong>" + esc(s.nome) + "</strong>" +
          " <span class='mini'>(versão " + esc(s.versao_atual) + ")</span>" + selo + "</li>";
      });
    });
    const notaAntecipada = qtdAntecipadas
      ? "<p class='mini' style='margin-top:10px; border-left:3px solid #c9a227; padding-left:10px'>" +
        "<strong>" + qtdAntecipadas + " delas estão marcadas como acesso antecipado.</strong> " +
        "São skills que ainda não foram lançadas para o público e estão liberadas na sua conta. " +
        "Elas já vêm no instalador e funcionam igual às outras: a diferença é que ainda não " +
        "passaram por uso real, então revise antes de protocolar e conte pra gente o que achar." +
        "</p>"
      : "";

    // Quem tem o catálogo completo precisa VER que é completo. Antes a aba
    // mostrava só uma lista de nomes, e a pessoa não tinha como saber se aquilo
    // era tudo o que existe ou um pedaço.
    const emBreve = dados.skills_em_breve || [];
    const temTudo = !(dados.skills_bloqueadas || []).length;
    const nomesDeArea = Array.from(porArea.keys())
      .filter((a) => a !== "universal").map(rotuloArea);
    const listaDeAreas = nomesDeArea.length > 1
      ? nomesDeArea.slice(0, -1).join(", ") + " e " + nomesDeArea[nomesDeArea.length - 1]
      : (nomesDeArea[0] || "");
    const cabecalho = temTudo
      ? "<h3>Você tem o catálogo completo</h3>" +
        "<p class='mini'>Todas as " + skills.length + " skills publicadas hoje" +
        (listaDeAreas ? ": " + esc(listaDeAreas) + ", mais as que servem para qualquer área" : "") +
        ". Tudo isso entra junto no instalador acima: instalou, tá tudo dentro.</p>"
      : "<h3>O que vem no seu pacote</h3>" +
        "<p class='mini'>Tudo isso entra junto no instalador acima. Instalou, tá tudo dentro.</p>";

    const rodapeEmBreve = (emBreve.length && emBreve.some((s) => s.inclusa_no_seu_plano))
      ? "<p class='mini' style='margin-top:14px; border-left:3px solid rgba(255,255,255,.2); padding-left:10px'>" +
        "Outras <strong>" + emBreve.length + " skills</strong> estão em construção, sem data prometida. " +
        "Quando ficarem prontas, entram no seu instalador sem você pagar de novo. " +
        "A lista completa está na aba <strong>Guia das skills</strong>.</p>"
      : "";

    box.innerHTML =
      cabecalho +
      "<ul style='margin:8px 0 0 18px; line-height:1.7;'>" + itens + "</ul>" +
      notaAntecipada + rodapeEmBreve;
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
  const emBreve = dados.skills_em_breve || [];
  if (!skills.length) {
    box.innerHTML = "<p class='vazio'>Nenhuma skill liberada ainda.</p>";
    return;
  }

  const rotulo = rotuloArea;

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

  // Mesma regra de agrupamento da aba Downloads.
  const porArea = agruparPorArea(skills);
  const areas = Array.from(porArea.keys());

  // Cabeçalho: diz de cara quantas áreas a pessoa tem na mão.
  const quantas = areas.filter((a) => a !== "universal").length;
  const resumo = document.createElement("p");
  resumo.className = "mini";
  resumo.style.margin = "18px 2px 6px";
  resumo.innerHTML = "Você tem <strong>" + skills.length + " skills</strong> em <strong>" +
    quantas + (quantas === 1 ? " área" : " áreas") + "</strong> do direito. Cada uma abaixo vem com os comandos prontos.";
  box.appendChild(resumo);

  areas.forEach((a) => {
    const titulo = document.createElement("h3");
    titulo.style.cssText = "margin:26px 0 10px; padding-bottom:6px; border-bottom:1px solid rgba(255,255,255,.12);";
    titulo.innerHTML = esc(rotulo(a)) +
      " <span class='mini' style='font-weight:400'>(" + porArea.get(a).length +
      (porArea.get(a).length === 1 ? " skill" : " skills") + ")</span>";
    box.appendChild(titulo);

    porArea.get(a).forEach((s) => {
      const info = guia[s.skill_id];
      const det = document.createElement("details");
      det.className = "card";
      // ⛔ ABERTO por padrão. Fechado, a pessoa via só o título e concluía que a
      // skill não tinha comando nenhum. O conteúdo é o que ela veio buscar aqui.
      det.open = true;
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
      const qtd = (info && info.funcoes) ? info.funcoes.length : 0;
      det.innerHTML =
        "<summary style='cursor:pointer; font-weight:700; font-size:1.05em;'>" +
        esc(s.nome) +
        " <span class='mini'>(" + (qtd ? qtd + (qtd === 1 ? " função própria" : " funções próprias") : "resumo") + ")</span></summary>" +
        "<p class='mini' style='margin-top:6px;'>" + esc((s.descricao || "").split(".")[0]) +
        ". Além das funções abaixo, esta skill tem todas as ferramentas dos blocos no fim da página.</p>" +
        corpo;
      box.appendChild(det);
    });
  });

  // O que ainda não saiu. Só aparece para quem tem alguma, e o texto muda
  // conforme a pessoa já ter direito a elas ou não.
  const inclusas = emBreve.some((s) => s.inclusa_no_seu_plano);
  if (emBreve.length && inclusas) {
    const porAreaBreve = new Map();
    emBreve.forEach((s) => {
      const a = s.area || "outras";
      if (!porAreaBreve.has(a)) porAreaBreve.set(a, []);
      porAreaBreve.get(a).push(s.nome);
    });
    const linhas = Array.from(porAreaBreve.entries())
      .sort((x, y) => rotulo(x[0]).localeCompare(rotulo(y[0]), "pt-BR"))
      .map(([a, nomes]) =>
        "<li style='margin-bottom:8px;'><strong>" + esc(rotulo(a)) + ":</strong> " +
        esc(nomes.join(", ")) + "</li>")
      .join("");

    const card = document.createElement("div");
    card.className = "card";
    card.style.marginTop = "28px";
    card.innerHTML =
      "<h3>As áreas que ainda estão por vir</h3>" +
      "<p class='mini' style='margin-top:6px;'>" +
      "Estas estão em construção, sem data prometida. Quando ficarem prontas, <strong>entram no seu acesso sem você pagar de novo</strong>." +
      "</p>" +
      "<ul style='margin:12px 0 0 18px; line-height:1.7;'>" + linhas + "</ul>";
    box.appendChild(card);
  }
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

// ---------- Upgrade do pacote ----------
// ⛔ O caminho de comprar outra área não existia em lugar nenhum do produto: quem
// usa todo dia e quer mais só conseguia comprar se alguém falasse com ele por
// fora. São as pessoas mais fáceis de vender, e elas não tinham para onde clicar.
//
// ⛔ Sem preço escrito aqui: preço muda, e número velho na área de membros faz o
// cliente chegar no checkout com outro valor e desistir. Quem mostra preço é a
// página da área, que é a fonte.
const AREAS_MAESTRIA = [
  {
    id: "prev",
    nome: "Previdenciário",
    texto: "Cálculo de atrasados e RMI, petição, impugnação de laudo, quesitos de perícia e recurso ao INSS.",
    pagina: "https://maestria.samurailab.com.br/prev/",
  },
  {
    id: "trab",
    nome: "Trabalhista",
    texto: "Cálculo trabalhista, petição inicial, contestação e acordo, com a conta e a peça no mesmo lugar.",
    pagina: "https://maestria.samurailab.com.br/trab/",
  },
  {
    id: "marketing",
    nome: "Marketing Jurídico",
    texto: "Reel, carrossel, estático, artigo e landing na sua voz, com a blindagem do Provimento 205 da OAB.",
    pagina: "https://maestria.samurailab.com.br/marketing/",
  },
];

function areasDoPlano(plano) {
  const p = String(plano || "").toLowerCase();
  // Quem é full, vitalício, black ou cortesia já tem tudo: nada a oferecer.
  if (["full", "vitalicio", "black", "cortesia"].some((x) => p.includes(x))) return "TUDO";
  if (!p.startsWith("pacote_")) return [];
  return p.replace("pacote_", "").split("_").filter(Boolean);
}

function montarUpgrade(dados, jaInstalou) {
  const caixa = $("ini-upgrade");
  if (!caixa) return;
  const plano = dados && dados.cliente ? dados.cliente.plano : "";
  const tem = areasDoPlano(plano);

  // ⛔ Não aparece para quem ainda está instalando, nem para quem já tem tudo.
  if (!jaInstalou || tem === "TUDO") {
    caixa.classList.add("hidden");
    return;
  }
  const faltam = AREAS_MAESTRIA.filter((a) => tem.indexOf(a.id) === -1);
  if (!faltam.length) {
    caixa.classList.add("hidden");
    return;
  }
  caixa.classList.remove("hidden");

  const nomesTem = AREAS_MAESTRIA.filter((a) => tem.indexOf(a.id) !== -1).map((a) => a.nome);
  const resumo = $("up-resumo");
  if (resumo) {
    resumo.textContent = nomesTem.length
      ? "Você tem " + listaBonita(nomesTem) + ". Dá para somar:"
      : "Dá para somar ao seu pacote:";
  }

  const grade = $("up-grade");
  if (!grade) return;
  grade.innerHTML =
    AREAS_MAESTRIA.map((a) => {
      const possui = tem.indexOf(a.id) !== -1;
      return (
        '<div class="up-item' + (possui ? " up-item--tem" : "") + '">' +
        (possui ? '<span class="up-tag">JÁ É SEU</span>' : "") +
        "<strong>" + esc(a.nome) + "</strong>" +
        "<p>" + esc(a.texto) + "</p>" +
        (possui
          ? ""
          : '<a class="up-btn" href="' + a.pagina + '?src=membros-upgrade" target="_blank" rel="noopener">Ver o ' +
            esc(a.nome) + "</a>") +
        "</div>"
      );
    }).join("");
}

function listaBonita(nomes) {
  if (nomes.length === 1) return nomes[0];
  return nomes.slice(0, -1).join(", ") + " e " + nomes[nomes.length - 1];
}

// ---------- Suporte ----------
// ⛔ O suporte e o GRUPO, e so. O formulario de chamado saiu da tela em
// 20/10/2026 ("isso nao existe, e tudo no grupo"): prometia resposta por
// e-mail em 48h que ninguem atendia. O codigo que o alimentava sai junto,
// porque $("form-ticket") sem o formulario no HTML derrubaria o resto do JS.
// Os chamados antigos continuam no banco e sao respondidos pelo admin.

// ---------- sessão persistida ----------
(async function init() {
  const cred = credenciais();
  if (cred && cred.token) {
    await entrar(cred.token, cred.cpf, false);
  }
})();
