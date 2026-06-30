// Calculadora ROI interativa - MaestrIA
(function() {
  'use strict';

  const SKILLS = {
    'peticao-builder': { nome: 'Petition Builder', economia_h: 2.6, frequencia: 5 },
    'calculo-previdenciario': { nome: 'Cálculo Previdenciário', economia_h: 1.85, frequencia: 3 },
    'calculo-trabalhista': { nome: 'Cálculo Trabalhista', economia_h: 1.85, frequencia: 2 },
    'marketing-juridico': { nome: 'Marketing Jurídico', economia_h: 2.35, frequencia: 3 },
    'briefing-do-caso': { nome: 'Briefing do Caso', economia_h: 0.55, frequencia: 3 },
    'pensao-alimenticia': { nome: 'Pensão Alimentícia', economia_h: 1.2, frequencia: 2 },
    'distrato-imobiliario': { nome: 'Distrato Imobiliário', economia_h: 1.2, frequencia: 1 },
    'habeas-corpus': { nome: 'Habeas Corpus', economia_h: 2.5, frequencia: 1 },
    'acordo-trabalhista': { nome: 'Acordo Trabalhista', economia_h: 1.0, frequencia: 2 },
    'divorcio-consensual': { nome: 'Divórcio Consensual', economia_h: 1.7, frequencia: 1 },
    'locacao-residencial': { nome: 'Locação (Despejo/Cobrança)', economia_h: 1.4, frequencia: 1 },
    'auditor-previdenciario': { nome: 'Auditor Previdenciário', economia_h: 2.0, frequencia: 2 },
    'contestacao-trabalhista': { nome: 'Contestação Trabalhista', economia_h: 2.8, frequencia: 1 },
    'recurso-administrativo-inss': { nome: 'Recurso Admin INSS', economia_h: 1.8, frequencia: 1 },
  };

  function fmtBRL(v) {
    return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 0 });
  }

  function calcular() {
    const valorHora = parseFloat(document.getElementById('calc-valor-hora').value) || 250;
    const semanasAno = 48;

    let economiaSemanaTotal = 0;
    document.querySelectorAll('.calc-skill-row input[type="checkbox"]:checked').forEach(cb => {
      const id = cb.dataset.skill;
      const skill = SKILLS[id];
      const freq = parseFloat(document.querySelector(`input[data-freq="${id}"]`).value) || skill.frequencia;
      economiaSemanaTotal += skill.economia_h * freq;
    });

    const economiaMes = economiaSemanaTotal * 4.33;
    const economiaAno = economiaSemanaTotal * semanasAno;
    const valorMes = economiaMes * valorHora;
    const valorAno = economiaAno * valorHora;
    const custoFull = 1997;
    const roi = valorAno > 0 ? (valorAno / custoFull).toFixed(0) : 0;

    document.getElementById('calc-result-h-semana').textContent = economiaSemanaTotal.toFixed(1) + 'h';
    document.getElementById('calc-result-h-mes').textContent = economiaMes.toFixed(0) + 'h';
    document.getElementById('calc-result-h-ano').textContent = economiaAno.toFixed(0) + 'h';
    document.getElementById('calc-result-valor-mes').textContent = fmtBRL(valorMes);
    document.getElementById('calc-result-valor-ano').textContent = fmtBRL(valorAno);
    document.getElementById('calc-result-roi').textContent = roi + 'x';
  }

  function montar() {
    const container = document.getElementById('calc-skills-list');
    if (!container) return;

    Object.entries(SKILLS).forEach(([id, s]) => {
      const row = document.createElement('div');
      row.className = 'calc-skill-row';
      row.innerHTML = `
        <label class="calc-skill-label">
          <input type="checkbox" data-skill="${id}" checked />
          <span class="calc-skill-nome">${s.nome}</span>
          <span class="calc-skill-eco">economia ${s.economia_h}h/uso</span>
        </label>
        <div class="calc-skill-freq">
          <label>Usos por semana:</label>
          <input type="number" data-freq="${id}" value="${s.frequencia}" min="0" max="50" step="1" />
        </div>
      `;
      container.appendChild(row);
    });

    document.querySelectorAll('#calculadora input').forEach(el => {
      el.addEventListener('input', calcular);
      el.addEventListener('change', calcular);
    });

    calcular();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', montar);
  } else {
    montar();
  }
})();
