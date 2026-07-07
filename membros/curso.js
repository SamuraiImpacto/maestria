// ============================================
// CURSO MAESTRIA: renderizador e navegação
// ============================================
// Renderiza os módulos de window.CURSO_MAESTRIA (conteudo.js) no layout
// de plataforma: os módulos viram itens do menu lateral principal
// (#menu-aulas) e a aula abre na view #view-aula. Componentes: terminal
// copiável, caixas de DICA/ATENÇÃO/NUNCA, checklists persistentes e exercícios.

(function () {
  "use strict";

  var CURSO = window.CURSO_MAESTRIA || [];
  var LS_PROGRESSO = "maestria_curso_progresso"; // { slug: true }
  var LS_CHECKS = "maestria_curso_checks";       // { "slug:idx": true }

  function lerLS(chave) {
    try { return JSON.parse(localStorage.getItem(chave) || "{}"); }
    catch (e) { return {}; }
  }
  function gravarLS(chave, obj) {
    try { localStorage.setItem(chave, JSON.stringify(obj)); } catch (e) {}
  }

  function esc(t) {
    return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Inline: **negrito**, *itálico*, `código`, [texto](url)
  function inline(t) {
    var s = esc(t);
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return s;
  }

  function caixaTipo(linha) {
    if (/^\*\*DICA:?\*\*/i.test(linha)) return ["dica", "DICA"];
    if (/^\*\*ATEN[ÇC][AÃ]O:?\*\*/i.test(linha)) return ["atencao", "ATENÇÃO"];
    if (/^\*\*NUNCA:?\*\*/i.test(linha)) return ["nunca", "NUNCA"];
    return null;
  }

  // Renderiza o markdown do módulo pros componentes do curso
  function render(md, slug) {
    var linhas = md.split("\n");
    var html = [];
    var i = 0;
    var checkIdx = 0;
    var checks = lerLS(LS_CHECKS);
    var dentroExercicio = false;

    function fecharExercicio() {
      if (dentroExercicio) { html.push("</div>"); dentroExercicio = false; }
    }

    while (i < linhas.length) {
      var l = linhas[i];
      var crua = l.trim();

      if (!crua) { i++; continue; }

      // Bloco de código -> terminal com copiar
      if (crua.indexOf("```") === 0) {
        var corpo = [];
        i++;
        while (i < linhas.length && linhas[i].trim().indexOf("```") !== 0) {
          corpo.push(linhas[i]); i++;
        }
        i++;
        var texto = corpo.join("\n");
        html.push(
          '<div class="c-terminal"><div class="c-terminal-bar"><span></span><span></span><span></span>' +
          '<button type="button" class="c-copiar" data-copiar="' + esc(texto).replace(/"/g, "&quot;") + '">copiar</button></div>' +
          '<pre>' + esc(texto) + '</pre></div>'
        );
        continue;
      }

      // Títulos
      if (crua.indexOf("### ") === 0) { html.push("<h4>" + inline(crua.slice(4)) + "</h4>"); i++; continue; }
      if (crua.indexOf("## ") === 0) {
        fecharExercicio();
        var titulo = crua.slice(3);
        var m = titulo.match(/^(\d+)\.\s*(.*)$/);
        if (/^Exerc[íi]cio/i.test(titulo)) {
          html.push('<div class="c-exercicio"><div class="c-exercicio-tag">EXERCÍCIO PRÁTICO</div>');
          dentroExercicio = true;
          if (titulo.replace(/^Exerc[íi]cio( final do curso| pr[áa]tico)?/i, "").trim()) {
            html.push("<h3>" + inline(titulo) + "</h3>");
          }
        } else if (/^Checklist/i.test(titulo)) {
          html.push('<h3 class="c-check-titulo">' + inline(titulo) + "</h3>");
        } else if (m) {
          html.push('<div class="c-kicker">' + m[1] + "</div><h3>" + inline(m[2]) + "</h3>");
        } else {
          html.push("<h3>" + inline(titulo) + "</h3>");
        }
        i++; continue;
      }

      // Caixas DICA/ATENÇÃO/NUNCA (blockquote)
      if (crua.indexOf(">") === 0) {
        var conteudo = [];
        while (i < linhas.length && linhas[i].trim().indexOf(">") === 0) {
          conteudo.push(linhas[i].trim().replace(/^>\s?/, "")); i++;
        }
        var junto = conteudo.join(" ").trim();
        var tipo = caixaTipo(junto);
        if (tipo) {
          var corpoCaixa = junto.replace(/^\*\*[^*]+\*\*:?\s*/, "");
          html.push('<div class="c-caixa c-caixa-' + tipo[0] + '"><span class="c-caixa-tag">' + tipo[1] + "</span><p>" + inline(corpoCaixa) + "</p></div>");
        } else {
          html.push('<blockquote class="c-quote">' + inline(junto) + "</blockquote>");
        }
        continue;
      }

      // Tabela
      if (crua.indexOf("|") === 0) {
        var tab = [];
        while (i < linhas.length && linhas[i].trim().indexOf("|") === 0) { tab.push(linhas[i].trim()); i++; }
        var rows = tab.filter(function (r) { return !/^\|[\s:|-]+\|$/.test(r); });
        var out = '<div class="c-tabela-wrap"><table>';
        rows.forEach(function (r, idx) {
          var cels = r.replace(/^\||\|$/g, "").split("|");
          out += "<tr>" + cels.map(function (c) {
            return (idx === 0 ? "<th>" : "<td>") + inline(c.trim()) + (idx === 0 ? "</th>" : "</td>");
          }).join("") + "</tr>";
        });
        out += "</table></div>";
        html.push(out);
        continue;
      }

      // Checklist persistente
      if (/^- \[[ x]\]/i.test(crua)) {
        var itens = [];
        while (i < linhas.length && /^- \[[ x]\]/i.test(linhas[i].trim())) {
          itens.push(linhas[i].trim().replace(/^- \[[ x]\]\s*/i, "")); i++;
        }
        var lista = '<ul class="c-checklist">';
        itens.forEach(function (item) {
          var chave = slug + ":" + checkIdx;
          var marcado = checks[chave] ? " checked" : "";
          lista += '<li><label><input type="checkbox" data-check="' + chave + '"' + marcado + "><span>" + inline(item) + "</span></label></li>";
          checkIdx++;
        });
        lista += "</ul>";
        html.push(lista);
        continue;
      }

      // Lista com marcador
      if (crua.indexOf("- ") === 0) {
        var li = [];
        while (i < linhas.length && linhas[i].trim().indexOf("- ") === 0) {
          li.push(linhas[i].trim().slice(2)); i++;
        }
        html.push("<ul>" + li.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ul>");
        continue;
      }

      // Lista numerada
      if (/^\d+\.\s/.test(crua)) {
        var lin = [];
        while (i < linhas.length && /^\d+\.\s/.test(linhas[i].trim())) {
          lin.push(linhas[i].trim().replace(/^\d+\.\s/, "")); i++;
        }
        html.push("<ol>" + lin.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</ol>");
        continue;
      }

      // Parágrafo
      html.push("<p>" + inline(crua) + "</p>");
      i++;
    }
    fecharExercicio();
    return html.join("\n");
  }

  // ---------- Menu lateral e navegação ----------

  function progresso() { return lerLS(LS_PROGRESSO); }

  // Preenche o grupo Aulas do menu lateral principal
  function montarMenu(ativo) {
    var alvo = document.getElementById("menu-aulas");
    if (!alvo) return;
    var prog = progresso();
    alvo.innerHTML = CURSO.map(function (mod) {
      var cls = "menu-item menu-aula" + (mod.slug === ativo ? " ativo" : "") + (prog[mod.slug] ? " feito" : "");
      return '<button type="button" class="' + cls + '" data-modulo="' + mod.slug + '">' +
        '<span class="menu-icone">' + mod.icone + "</span><span>" + esc(mod.titulo.split(":")[0]) + "</span>" +
        (prog[mod.slug] ? '<span class="menu-check">✓</span>' : "") + "</button>";
    }).join("");
    alvo.querySelectorAll("[data-modulo]").forEach(function (b) {
      b.addEventListener("click", function () { abrirModulo(b.getAttribute("data-modulo")); });
    });
  }

  function abrirModulo(slug) {
    var mod = CURSO.filter(function (m) { return m.slug === slug; })[0] || CURSO[0];
    if (!mod) return;
    var idx = CURSO.indexOf(mod);
    var tela = document.getElementById("view-aula");
    var anterior = CURSO[idx - 1];
    var proximo = CURSO[idx + 1];

    tela.innerHTML =
      '<article class="c-aula"><p class="c-aula-modulo">Aula ' + mod.ordem + " de " + (CURSO.length - 1) + "</p>" +
      "<h2>" + esc(mod.titulo) + "</h2><p class=\"c-aula-sub\">" + esc(mod.subtitulo) + "</p>" +
      render(mod.corpo, mod.slug) +
      '<div class="c-nav">' +
      (anterior ? '<button type="button" class="c-nav-ant" data-modulo="' + anterior.slug + '">← ' + esc(anterior.titulo.split(":")[0]) + "</button>" : "<span></span>") +
      '<button type="button" class="c-nav-prox" data-modulo="' + (proximo ? proximo.slug : "") + '">' +
      (proximo ? "Concluir e ir pra próxima →" : "Concluir o curso ✓") + "</button></div></article>";

    montarMenu(mod.slug);
    if (window.MAESTRIA_VIEW) window.MAESTRIA_VIEW.mostrar("aula");

    // Eventos: navegação anterior/próxima
    tela.querySelectorAll(".c-nav-ant, .c-nav-prox").forEach(function (b) {
      b.addEventListener("click", function () {
        if (b.classList.contains("c-nav-prox")) marcarConcluido(mod.slug);
        var destino = b.getAttribute("data-modulo");
        if (destino) {
          abrirModulo(destino);
        } else {
          montarMenu(mod.slug); // atualiza o check da última aula
          if (window.MAESTRIA_VIEW) window.MAESTRIA_VIEW.mostrar("downloads");
        }
      });
    });

    tela.querySelectorAll(".c-copiar").forEach(function (b) {
      b.addEventListener("click", function () {
        var texto = b.getAttribute("data-copiar");
        if (navigator.clipboard) navigator.clipboard.writeText(texto);
        b.textContent = "copiado!";
        setTimeout(function () { b.textContent = "copiar"; }, 1600);
      });
    });

    tela.querySelectorAll("[data-check]").forEach(function (c) {
      c.addEventListener("change", function () {
        var checks = lerLS(LS_CHECKS);
        if (c.checked) checks[c.getAttribute("data-check")] = true;
        else delete checks[c.getAttribute("data-check")];
        gravarLS(LS_CHECKS, checks);
      });
    });
  }

  function marcarConcluido(slug) {
    var prog = progresso();
    prog[slug] = true;
    gravarLS(LS_PROGRESSO, prog);
  }

  // Primeira entrada: abre a primeira aula ainda não concluída
  function abrirInicial() {
    var prog = progresso();
    var pendente = CURSO.filter(function (m) { return !prog[m.slug]; })[0];
    abrirModulo((pendente || CURSO[0] || {}).slug);
  }

  window.MAESTRIA_CURSO = { abrir: abrirModulo, montarMenu: montarMenu, abrirInicial: abrirInicial };
})();
