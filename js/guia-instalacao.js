// Controles do guia visual. Os tempos vêm do vídeo renderizado em 23/10/2026.
(function () {
  "use strict";
  const video = document.getElementById("tutorial");
  const capitulos = {"03": 77.4, "06": 173.6, "08": 267.8, "10": 331.8};
  document.querySelectorAll("[data-tempo], [data-cena]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      if (!video) return;
      video.currentTime = Number(botao.dataset.tempo ?? capitulos[botao.dataset.cena]);
      video.focus();
      const inicio = video.play();
      if (inicio && inicio.catch) inicio.catch(function () { /* O botão do vídeo continua disponível. */ });
    });
  });
  document.querySelectorAll("[data-copiar]").forEach(function (botao) {
    botao.addEventListener("click", async function () {
      const texto = botao.dataset.copiar;
      const rotulo = botao.textContent;
      try {
        await navigator.clipboard.writeText(texto);
        botao.textContent = "Copiado!";
      } catch (_) {
        botao.textContent = "Selecione e copie o texto ao lado";
      }
      setTimeout(function () { botao.textContent = rotulo; }, 4000);
    });
  });
})();
