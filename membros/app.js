// MaestrIA Área de Membros
// Login: código de ativação + CPF -> edge member-area (Supabase Core).
// Nenhuma chave secreta aqui: a edge valida token + CPF por conta própria.

const CORE = "https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1";

const $ = (id) => document.getElementById(id);

// ---------- utilitários ----------
function mascaraCpf(valor) {
  const d = valor.replace(/\D/g, "").slice(0, 11);
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

// ---------- login ----------
$("inp-cpf").addEventListener("input", (e) => {
  e.target.value = mascaraCpf(e.target.value);
});

$("form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = $("inp-token").value.trim();
  const cpf = $("inp-cpf").value.replace(/\D/g, "");
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

  // Skills
  const grid = $("pl-skills");
  grid.innerHTML = "";
  (dados.skills || []).forEach((s) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML =
      "<h3>" + esc(s.nome) + " <span class='versao'>v" + esc(s.versao_atual) + "</span></h3>" +
      "<p>" + esc((s.descricao || "").split(".")[0]) + ".</p>" +
      "<a class='btn-baixar' href='" + esc(s.zip_url) + "'>Baixar ZIP</a>" +
      (s.changelog
        ? "<details><summary>O que há de novo</summary><p>" + esc(s.changelog) + "</p></details>"
        : "");
    grid.appendChild(card);
  });

  // Licença
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
    ul.innerHTML = "<li>Nenhum computador ativado ainda. Rode /maestria ativar na skill instalada.</li>";
  } else {
    maquinas.forEach((m) => {
      const li = document.createElement("li");
      li.textContent = m.hostname + (m.os_info ? " (" + m.os_info + ")" : "") + " desde " + dataBr(m.ativada_em);
      ul.appendChild(li);
    });
  }

  // Chamados
  renderizarTickets(dados.tickets || []);

  // Select de skill do formulário de chamado
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
