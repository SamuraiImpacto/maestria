"use strict";
(function () {
  const modelos = [...document.querySelectorAll(".modelo")];
  const busca = document.querySelector("#busca");
  const contador = document.querySelector("#contador");
  const vazio = document.querySelector("#vazio");
  const dialogo = document.querySelector("#ampliacao");
  let filtro = "todos";
  let origem = null;
  const normalizar = texto => texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  function filtrar() {
    const termo = normalizar(busca.value.trim());
    let visiveis = 0;
    modelos.forEach(modelo => {
      const foto = Number(modelo.dataset.fotos);
      const corresponde = filtro === "todos" || (filtro === "sem-foto" ? foto === 0 : foto > 0);
      modelo.hidden = !(corresponde && normalizar(modelo.dataset.busca).includes(termo));
      if (!modelo.hidden) visiveis++;
    });
    contador.textContent = `${visiveis} de ${modelos.length} modelos. Toque em uma arte para ampliar.`;
    vazio.hidden = visiveis > 0;
  }
  document.querySelectorAll("[data-formato-escolha]").forEach(botao => {
    botao.addEventListener("click", () => {
      document.body.dataset.formato = botao.dataset.formatoEscolha;
      document.querySelectorAll("[data-formato-escolha]").forEach(outro => outro.setAttribute("aria-pressed", String(outro === botao)));
    });
  });
  document.querySelectorAll("[data-filtro]").forEach(botao => {
    botao.addEventListener("click", () => {
      filtro = botao.dataset.filtro;
      document.querySelectorAll("[data-filtro]").forEach(outro => outro.setAttribute("aria-pressed", String(outro === botao)));
      filtrar();
    });
  });
  busca.addEventListener("input", filtrar);
  document.querySelectorAll("[data-ampliar]").forEach(botao => {
    botao.addEventListener("click", () => {
      const imagem = botao.querySelector("img");
      const ampliada = dialogo.querySelector("img");
      ampliada.src = imagem.src;
      ampliada.alt = imagem.alt;
      document.querySelector("#titulo-ampliacao").textContent = imagem.alt;
      origem = botao;
      dialogo.showModal();
    });
  });
  document.querySelector("#fechar-ampliacao").addEventListener("click", () => dialogo.close());
  dialogo.addEventListener("close", () => { if (origem) origem.focus(); });
  filtrar();
})();
