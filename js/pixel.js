/* Meta Pixel do MaestrIA. Arquivo único, carregado por todas as páginas
   públicas, pra trocar o ID em um lugar só quando precisar.

   Pixel: Pixel Advogads | Samurai Lab (conta CA - Advogads Principal).

   Purchase NÃO dispara aqui de propósito: quem tem o valor real da venda é a
   Kiwify. Plugar o pixel no painel dela evita disparo duplicado e valor errado.
*/
(function () {
  var PIXEL_ID = "347471045036495";

  /* snippet oficial do Meta */
  !function (f, b, e, v, n, t, s) {
    if (f.fbq) return; n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0";
    n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
    s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
  }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");

  fbq("init", PIXEL_ID);
  fbq("track", "PageView");

  /* Valor de cada checkout, pro Meta otimizar por receita e não por clique.
     A chave é o código final da URL da Kiwify. */
  var CHECKOUTS = {
    mS2gAMm: { valor: 1997, nome: "Full Embaixador" },
    q5QEizf: { valor: 697, nome: "Pacote Previdenciario" },
    zRpxcta: { valor: 697, nome: "Pacote Trabalhista" },
    Ln4ErJJ: { valor: 697, nome: "Pacote Marketing Juridico" },
    Lvo0094: { valor: 997, nome: "Combo Previdenciario + Trabalhista" },
  };

  /* Delegação no document: pega o clique mesmo em botão criado depois,
     e funciona com o script carregando de forma assíncrona. */
  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest("a") : null;
    if (!a || !a.href) return;

    if (a.href.indexOf("pay.kiwify.com.br") > -1) {
      var codigo = a.href.split("?")[0].split("/").pop();
      var item = CHECKOUTS[codigo] || { valor: 0, nome: codigo };
      fbq("track", "InitiateCheckout", {
        content_name: item.nome,
        value: item.valor,
        currency: "BRL",
      });
    }
  });

  /* ViewContent quando o bloco de preço aparece na tela: sinal de intenção
     real, bem melhor que tempo de página pra alimentar o público quente. */
  function observarPlanos() {
    var alvo = document.getElementById("planos");
    if (!alvo || !window.IntersectionObserver) return;
    var obs = new IntersectionObserver(function (entradas) {
      for (var i = 0; i < entradas.length; i++) {
        if (entradas[i].isIntersecting) {
          fbq("track", "ViewContent", { content_name: "Planos MaestrIA" });
          obs.disconnect();
        }
      }
    }, { threshold: 0.3 });
    obs.observe(alvo);
  }

  /* Lead no envio do formulário de suporte. */
  function observarFormulario() {
    var forms = document.querySelectorAll("form");
    for (var i = 0; i < forms.length; i++) {
      forms[i].addEventListener("submit", function () {
        fbq("track", "Lead");
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      observarPlanos(); observarFormulario();
    });
  } else {
    observarPlanos(); observarFormulario();
  }
})();
