# O que falta na Black do MaestrIA Marketing (handoff)

A pagina esta pronta e no ar em https://maestria.samurailab.com.br/black/
Arquivo unico: `black/index.html`. Nao ha build, nao ha dependencia.

## 1. Os dois links que faltam (2 minutos, e so isto)

Abra `black/index.html` e procure `window.BLACK` nas primeiras 40 linhas.
Cole os checkouts nos dois campos vazios:

    marketingPrev:  "",   <- Marketing + Previdenciario (R$ 997)
    marketingTrab:  "",   <- Marketing + Trabalhista (R$ 997)

O de R$ 297 ja esta preenchido. Enquanto um campo estiver vazio, o botao daquele
plano aparece apagado escrito "Link em instantes", de proposito: botao que leva a
lugar nenhum perde a venda e nao avisa ninguem.

Depois: `git add -A && git commit -m "Black: links dos combos" && git push`
O deploy sai sozinho em ~6 min, ou na hora com o MAESTRIA_DEPLOY_HOOK do cofre.

## 2. O prazo

No mesmo `window.BLACK`, o campo `fim` esta em 2026-10-22T23:59:59-03:00.
A pagina vira sozinha quando passa: a faixa muda, o contador some, o preco
riscado some e aparece o aviso de encerrada. Se a Black esticar, mude a data ali.

## 3. O VSL (nao feito, e por que)

O Samurai pediu um VSL motion com voz humana. Nao entreguei porque:

- a voz precisa de TTS pago e de boa qualidade; voz robotizada numa pagina de
  venda faz mais mal do que nao ter video;
- o motor do editor (`maestria-editor-motor`) faz o motion, mas NAO faz voz;
- a memoria do projeto diz que clipe de IA esta suspenso ate o Samurai saber o
  custo (`IA_LIBERADA=1`), e gerar voz paga sem ele autorizar quebraria isso.

Quando houver decisao de custo, o caminho mais curto e:
1. roteiro de 60 a 90 s a partir da propria pagina (as secoes ja estao na ordem);
2. voz em TTS bom (ElevenLabs ou equivalente), em portugues do Brasil;
3. motion pelo proprio editor da MaestrIA (`/anuncio-sem-gravar` faz telas em
   motion nos tres tamanhos) ou pelo HyperFrames direto;
4. subir o arquivo e colar a URL em `window.BLACK.vsl`. A pagina ja aceita tanto
   link de embed (YouTube/Vimeo) quanto arquivo .mp4 direto, e so mostra o player
   quando o campo existir.

## 4. O que NAO precisa mexer

Textos, precos, perguntas e a identidade visual ja batem com as outras LPs
(mesma paleta, Playfair + Inter, mesmo favicon e OG). A pagina foi conferida no
navegador: contador rodando, 3 planos, 15 cartoes de entregavel, 6 perguntas.
