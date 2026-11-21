# Ferramentas do site

Esta pasta não vai para o ar: o Dockerfile só copia as pastas que ele cita.

## gerar_teste_areas.py

Gera a página do teste grátis de cada área a partir de uma base só.

```bash
python _ferramentas/gerar_teste_areas.py
```

- `teste-base.html`: a página do teste como foi aprovada. Mudança de texto ou de visual que vale para todas as áreas se faz aqui.
- `areas.json`: título, frase e ferramentas de cada área.
- As demonstrações de petição, cálculo e jurisprudência vêm da página de venda de cada pacote (`/familia/`, `/criminal/` e as outras).

Depois de rodar, confira `teste/index.html` e as sete pastas `teste/<area>/`. Não edite essas páginas à mão: a próxima geração apaga a mudança.

## Dois cuidados que já custaram um deploy

- Se mudar um texto de `teste-base.html` que o gerador usa como ponto de apoio, o gerador para com erro. Só faça o commit depois de ver a linha `teste/area/index.html: redirecionamento` no fim.
- Dois merges com menos de um minuto de intervalo: o EasyPanel publica o primeiro e ignora o segundo. Espere o primeiro aparecer no ar antes do próximo.

