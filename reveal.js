// Entrada suave dos blocos ao rolar a página (identidade MaestrIA).
// Aplica .rvl nos cards e blocos-chave e dispara .rvl-on quando entram na tela.
// Com prefers-reduced-motion o CSS neutraliza tudo (acessibilidade).
(function () {
  "use strict";
  if (!("IntersectionObserver" in window)) return;

  var alvos = document.querySelectorAll(
    ".dor-card, .pack-card, .cons-card, .passo-card, .roi-card, .pq-col, " +
    ".diff-col, .terminal-mock, .garantia-card, .roadmap-item, .prereq-box, .banco-ponto"
  );
  if (!alvos.length) return;

  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("rvl-on");
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });

  alvos.forEach(function (el, i) {
    el.classList.add("rvl");
    // escadinha sutil dentro do mesmo grupo visual
    el.style.transitionDelay = (i % 4) * 70 + "ms";
    obs.observe(el);
  });

  // FAIL-SAFE: conteúdo de venda nunca pode ficar escondido. Se por qualquer
  // motivo o observer não disparar (navegador raro, compositor travado),
  // revela tudo depois de 2,5s e segue o baile sem efeito.
  setTimeout(function () {
    if (!document.querySelector(".rvl-on")) {
      alvos.forEach(function (el) { el.classList.add("rvl-on"); });
      obs.disconnect();
    }
  }, 2500);
})();
