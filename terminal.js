// Animação do terminal de demonstração da MaestrIA.
// Digita os comandos, mostra a skill "pensando" e revela as respostas em sequência.
// Respeita prefers-reduced-motion (deixa o transcript estático).

document.addEventListener('DOMContentLoaded', function () {
  var body = document.querySelector('.terminal-body');
  if (!body) return;

  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  // Captura o roteiro a partir do HTML estático (fallback sem JS continua legível)
  var roteiro = Array.prototype.slice.call(body.children).map(function (el) {
    return { html: el.innerHTML, cls: el.className };
  });

  // Trava a altura final pra página não pular durante a animação
  body.style.minHeight = body.offsetHeight + 'px';

  function esperar(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  function criaLinha(cls) {
    var p = document.createElement('p');
    p.className = cls;
    body.appendChild(p);
    return p;
  }

  async function digitar(linha) {
    var tmp = document.createElement('div');
    tmp.innerHTML = linha.html;
    var promptEl = tmp.querySelector('.t-prompt');
    var texto = tmp.textContent.replace(/^>\s*/, '');

    var p = criaLinha(linha.cls);
    if (promptEl) p.innerHTML = promptEl.outerHTML + ' ';

    var cursor = document.createElement('span');
    cursor.className = 't-cursor';
    p.appendChild(cursor);

    await esperar(500);
    for (var i = 0; i < texto.length; i++) {
      cursor.insertAdjacentText('beforebegin', texto[i]);
      await esperar(50 + Math.random() * 70);
    }
    await esperar(400);
    cursor.remove();
  }

  async function pensar(ms) {
    var p = criaLinha('t-thinking');
    p.innerHTML = '<span></span><span></span><span></span>';
    await esperar(ms);
    p.remove();
  }

  async function responder(linha, pausaPensando) {
    await pensar(pausaPensando);
    var p = criaLinha(linha.cls + ' t-appear');
    p.innerHTML = linha.html;
    await esperar(650);
  }

  var rodando = false;

  async function rodar() {
    if (rodando) return;
    rodando = true;
    while (true) {
      body.innerHTML = '';
      for (var i = 0; i < roteiro.length; i++) {
        var linha = roteiro[i];
        if (linha.cls.indexOf('t-cmd') !== -1) {
          await digitar(linha);
        } else if (linha.cls.indexOf('t-ok') !== -1) {
          await responder(linha, 1600);
        } else if (linha.cls.indexOf('t-meta') !== -1) {
          await responder(linha, 500);
        } else {
          await responder(linha, 1100);
        }
      }
      await esperar(7000);
    }
  }

  var obs = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) {
      rodar();
      obs.disconnect();
    }
  }, { threshold: 0.35 });

  obs.observe(body);
});
