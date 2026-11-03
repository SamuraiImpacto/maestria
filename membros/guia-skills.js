// Gerado automaticamente a partir dos ZIPs PUBLICADOS no catalogo (nao editar a mao).
// Regenerar: python manutencao/gerar_guia_do_catalogo.py
// Depois de regenerar, BUMPAR o ?v= de guia-skills.js em membros/index.html.
window.MAESTRIA_GUIA = {
 "peticao-builder": {
  "funcoes": [
   {
    "c": "add-bloco",
    "d": "Salva uma jurisprudência ou trecho reutilizável VINCULADO a tipos de petição. Em toda /nova-peticao do tipo vinculado, eu pergunto se quer incluir. Cobre o uso real do advogado (reusar as mesmas juris em todas as peças do mesmo tipo)."
   },
   {
    "c": "add-cenario",
    "d": "Adicionar um cenário (sub-tipo) novo dentro de um tipo de petição existente. Exemplo: \"com dano moral\" dentro de \"auxílio-acidente\". Pede modelo Word específico desse cenário."
   },
   {
    "c": "add-tipo",
    "d": "Adicionar um novo tipo de petição na configuração do advogado. Pede um modelo real dele do tipo novo, extrai a estrutura e cria o template."
   },
   {
    "c": "buscar-jurisprudencia",
    "d": "Pesquisa precedentes e temas em fontes oficiais com as ferramentas do aplicativo, confere o conteúdo e prepara citações. Sem chave de serviço externo."
   },
   {
    "c": "configurar-revisor",
    "d": "Treina o revisor de peças com os critérios do PRÓPRIO advogado: lê 2 ou 3 peças que ele considera impecáveis, entrevista curta sobre o que ele sempre confere, e salva o checklist vivo do escritório. Roda uma vez; o /revisar-peca usa pra sempre."
   },
   {
    "c": "contribuir-banco-peticoes",
    "d": "Cliente doa modelos próprios pro Banco de Petições (modelos externos). Sanitização automática + envio pro cofre central de modelos. Voluntário, com benefício combinado."
   },
   {
    "c": "menos-perguntas",
    "d": "Liga o modo fluido, o Claude para de pedir permissão a cada passo da peticao-builder (escopado e seguro, sem liberar tudo)."
   },
   {
    "c": "modo-teste",
    "d": "Cria um CASO DEMO 100% fictício (cliente, CNIS, laudo, carta de concessão do INSS) pra você experimentar a MaestrIA de ponta a ponta sem usar dado de cliente real. Ideal pra testar, treinar a equipe ou gravar demonstração. Tudo marcado como FICTÍCIO."
   },
   {
    "c": "nova-peticao",
    "d": "Gera uma nova petição. Conduz intake guiado por tipo de peça, recebe prints, gera Word com formatação do modelo do escritório, salva local na pasta do caso."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "recalibrar",
    "d": "Recalibra o template de um tipo de petição existente, com modelo novo. Substitui ou enriquece o template atual."
   },
   {
    "c": "retomar",
    "d": "Retoma uma petição que ficou pela metade. Se a conversa reiniciou (nova conversa, Claude fechado, internet caiu), este comando encontra o caso salvo no disco e continua exatamente de onde parou. Nada se perde."
   },
   {
    "c": "revisar-peca",
    "d": "Revisa qualquer peça jurídica em 2 camadas: técnica universal (citações validadas em fonte oficial, requisitos da peça, coerência fato-fundamento-pedido) + o checklist vivo do advogado (/configurar-revisor). Parecer em Word com achados por severidade."
   },
   {
    "c": "setup-escritorio",
    "d": "Configura ou atualiza o perfil do escritório do advogado. Roda 1 vez na instalação, ou sempre que muda dados (mudou endereço, OAB nova, novo tipo de peça)."
   },
   {
    "c": "tirar-duvida",
    "d": "Responde uma dúvida jurídica rápida (de cliente, de colega ou de grupo) com precisão. Lista os fatos que faltam, dá a resposta curta, mostra a fonte oficial conferida com o link, separa o que é prática do INSS e entrega a versão pronta para colar no grupo."
   },
   {
    "c": "ver-banco-peticoes",
    "d": "Lista o que tem disponível no Banco de Petições (modelos externos, curados). Não revela origem dos modelos."
   }
  ]
 },
 "acao-consumidor": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Conduz intake e gera petição inicial de ação de consumidor (vício, propaganda, cobrança indevida)."
   }
  ]
 },
 "acao-medicamento": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Conduz intake e gera ação para fornecimento de medicamento ou tratamento."
   }
  ]
 },
 "acordo-trabalhista": {
  "funcoes": [
   {
    "c": "novo-acordo",
    "d": "Conduz cálculo de valor mínimo, negociação e redação de termo de acordo trabalhista."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "auditor-previdenciario": {
  "funcoes": [
   {
    "c": "auditar",
    "d": "Audita o CNIS do segurado vs documentos. Detecta gaps, indicadores e sugere ações de correção."
   },
   {
    "c": "coisa-julgada",
    "d": "O gate antes de protocolar. Descobre se o cliente já processou o INSS pelo mesmo pedido, aplica o teste da tríplice identidade e diz o caminho certo: protocolar, novo requerimento administrativo, ou rescisória. Evita a extinção do art. 485, V do CPC e a condenação em honorários."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "briefing-do-caso": {
  "funcoes": [
   {
    "c": "analisar-provas",
    "d": "Análise probatória do caso: recebe os autos e documentos e devolve o mapa de provas por fato controvertido: o que cada prova sustenta, onde ela é frágil, como a parte contrária vai atacar, que prova falta produzir e o plano de ação (testemunha, perícia, juntada), entregue em Word."
   },
   {
    "c": "briefing",
    "d": "Conduz briefing estruturado por tipo de atendimento. UMA pergunta por vez. Gera o documento em Word ao final."
   },
   {
    "c": "consultar-processo",
    "d": "Consulta o andamento de qualquer processo pelo número unificado, direto na base oficial do CNJ (DataJud): classe, órgão julgador, assuntos e a linha do tempo de movimentações, sem abrir o site do tribunal."
   },
   {
    "c": "pode-fazer",
    "d": "Responde se a MaestrIA faz alguma coisa, com o comando exato pra fazer. Quando NÃO faz, diz que não faz e oferece registrar o pedido. Nunca inventa comando."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "resumir-processo",
    "d": "Recebe os autos de um processo em andamento (PDF, mesmo grandão) e devolve a ficha executiva: partes, linha do tempo das decisões, estado atual, prazos em risco e próximos passos. O comando de quem pegou o caso pela metade."
   },
   {
    "c": "triagem-caso",
    "d": "Triagem do PRIMEIRO contato do cliente: joga a conversa de WhatsApp (texto ou áudio) e recebe: área do direito, urgência com alerta de prazo e prescrição, viabilidade preliminar, documentos a pedir e minuta de resposta pronta. O SDR jurídico rodando na sua máquina."
   }
  ]
 },
 "calculo-bancario": {
  "funcoes": [
   {
    "c": "calculo-revisional",
    "d": "Calcula a revisional de um contrato bancário, da taxa cobrada ao valor da causa, com a taxa média do Banco Central buscada na fonte."
   },
   {
    "c": "cumprimento-revisional-calculo",
    "d": "Monta o demonstrativo do art. 524 do CPC no cumprimento da revisional, aplicando o que o título mandou sobre as parcelas efetivamente pagas."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "taxa-bacen",
    "d": "Consulta a taxa média de mercado do Banco Central para uma modalidade e um mês, com a prova da fonte."
   }
  ]
 },
 "calculo-previdenciario": {
  "funcoes": [
   {
    "c": "atualizar-indices",
    "d": "Baixa as séries mensais oficiais (INPC, IPCA-E, Selic) do Banco Central e guarda no banco de índices da skill com fonte e data."
   },
   {
    "c": "calcular-atrasados",
    "d": "Calcula valores atrasados do benefício previdenciário (RMI × meses devidos) com correção monetária (INPC/IPCA-E até 11/2021) e juros por faixa de mora (1% am até 06/2009, poupança de 07/2009 a 11/2021, Selic exclusiva a partir de 12/2021)."
   },
   {
    "c": "calcular-auxilio-acidente",
    "d": "Calcula a RMI do auxílio-acidente a partir do valor do auxílio-doença na cessação (engenharia reversa, pra quando só se tem a carta de concessão) ou pelo caminho completo do CNIS. Avisa quando piso ou teto distorcem o atalho."
   },
   {
    "c": "calcular-rmi",
    "d": "Calcula Salário de Benefício (SB), fator previdenciário (se aplicável) e RMI (Renda Mensal Inicial)."
   },
   {
    "c": "caminho-acidente",
    "d": "Lê a negativa do INSS, o laudo da perícia do INSS (SABI) e o CNIS de um caso de auxílio-acidente e diz o caminho: pedido no INSS ou ação, qual Justiça, quais teses e quais documentos faltam, com o checklist do pedido administrativo exigido desde a Portaria Conjunta MPS/INSS 15/2026."
   },
   {
    "c": "comparar-beneficios",
    "d": "Compara, com as mesmas contribuições, auxílio-doença, aposentadoria por incapacidade e auxílio-acidente pela regra da data em que a incapacidade começou, e confere se o cálculo da contadoria do juízo aplicou a regra certa (antes ou depois da reforma de 13/11/2019)."
   },
   {
    "c": "jurimetria",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "planejamento-previdenciario",
    "d": "Planejamento previdenciário completo pra vender como consultoria. Projeta ano a ano quando cada regra de aposentadoria destrava, compara aposentar agora vs esperar, simula estratégias de contribuição (teto, plano simplificado, parar de contribuir) com custo-benefício, e entrega relatório em Word ..."
   },
   {
    "c": "qualificar-acidente",
    "d": "Triagem comercial de lead de auxílio-acidente pro time do escritório. Conduz o roteiro de perguntas (lesão, data, qualidade de segurado, função), roda o motor do período de graça e devolve o veredito PERFIL FORTE / INVESTIGAR / NÃO SERVE com o próximo passo pronto (script de fechamento ou desqual..."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "simular-beneficio",
    "d": "Simula os cenários de aposentadoria pós-EC 103/2019 (pontos, idade mínima progressiva, pedágio 50%, pedágio 100%, regra permanente por idade, especial) e mostra, pra cada regra, se o segurado já cumpre, o que falta e a estimativa de RMI."
   }
  ]
 },
 "calculo-trabalhista": {
  "funcoes": [
   {
    "c": "atualizar-indices",
    "d": "Baixa as séries mensais oficiais (Selic, INPC, IPCA-E, TR) do Banco Central e grava em data/indices_trab.json com fonte e data."
   },
   {
    "c": "calcular-adicional",
    "d": "Calcula adicional (insalubridade, periculosidade, noturno) + reflexos por período prescricional."
   },
   {
    "c": "calcular-fgts",
    "d": "Calcula diferenças FGTS (depósitos não realizados, multa 40%, expurgos)."
   },
   {
    "c": "calcular-he",
    "d": "Calcula horas extras + reflexos (DSR, 13º, férias, FGTS, multa 40%)."
   },
   {
    "c": "calcular-rescisao",
    "d": "Calcula verbas rescisórias (aviso prévio, 13º, férias, multa FGTS, saldo salário) com correção e juros."
   },
   {
    "c": "jurimetria",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "contestacao-trabalhista": {
  "funcoes": [
   {
    "c": "nova-contestacao",
    "d": "Conduz intake e gera contestação trabalhista atacando ponto a ponto cada pedido da inicial."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "dano-moral-consumidor": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Conduz intake e gera ação por dano moral em relação consumerista."
   }
  ]
 },
 "defesa-flagrante": {
  "funcoes": [
   {
    "c": "responder-apf",
    "d": "Conduz intake do auto de prisão em flagrante e gera resposta com pedido de relaxamento, liberdade provisória ou medida cautelar diversa."
   }
  ]
 },
 "defesa-trabalhista-empresa": {
  "funcoes": [
   {
    "c": "nova-defesa",
    "d": "Conduz intake da reclamatória e gera análise de defesa focada em proteção empresarial."
   }
  ]
 },
 "defesa-tributaria-administrativa": {
  "funcoes": [
   {
    "c": "impugnar-auto",
    "d": "Conduz intake do auto de infração e gera impugnação administrativa fundamentada."
   }
  ]
 },
 "distrato-imobiliario": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Gera petição de distrato, resolução, vícios construtivos ou restituição."
   }
  ]
 },
 "divorcio-consensual": {
  "funcoes": [
   {
    "c": "novo-divorcio",
    "d": "Conduz intake do divórcio consensual e prepara escritura/petição."
   }
  ]
 },
 "habeas-corpus": {
  "funcoes": [
   {
    "c": "impetrar-hc",
    "d": "Conduz intake e gera impetração de habeas corpus liberatório, preventivo ou trancamento."
   }
  ]
 },
 "impugnacao-laudo-pericial": {
  "funcoes": [
   {
    "c": "impugnar",
    "d": "Conduz intake e gera impugnação ao laudo pericial entregue em Word."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "impugnacao-ppp": {
  "funcoes": [
   {
    "c": "impugnar-ppp",
    "d": "Gera impugnação técnica ao PPP defeituoso, atacando os 8 vícios mais comuns."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "locacao-residencial": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Conduz intake de ação locatícia (despejo, cobrança, revisional, renovatória)."
   }
  ]
 },
 "marketing-juridico": {
  "funcoes": [
   {
    "c": "anuncio-sem-gravar",
    "d": "Cria vídeos animados com a marca do advogado, sem aparecer, com texto ou narração própria, sem conta extra ou chave. Mostra modelos reais, prepara a prévia e entrega MP4 em 9:16, 4:5 ou 1:1."
   },
   {
    "c": "calendario-editorial",
    "d": "Gera calendário editorial mensal (30 dias) com tema, formato e pilar FLG por dia."
   },
   {
    "c": "cardapio-carrossel",
    "d": "Abre o cardápio visual de modelos para carrosséis e estáticos, com prévias na marca do advogado, finalidade, quantidade de imagens e formatos aceitos. Salva o modelo preferido para as próximas peças."
   },
   {
    "c": "cardapio-video",
    "d": "Abre o cardápio de edição de vídeo do MaestrIA Marketing no navegador, com os modelos e vídeos de amostra distribuídos na versão instalada, para escolher olhando."
   },
   {
    "c": "carrossel-imagens",
    "d": "Desenha o texto aprovado em PNGs com imagens e a marca do advogado, usando o modelo preferido. Confere texto, legibilidade e composição e mostra as lâminas reais antes da entrega."
   },
   {
    "c": "cortes-video",
    "d": "Transforma uma gravação longa (live, aula, palestra, entrevista) em vários cortes curtos para o Instagram, cada um fechando uma ideia, editados com o modelo do cardápio."
   },
   {
    "c": "criar-site",
    "d": "Constrói o site profissional completo do advogado com poucas perguntas: rápido, preparado pro Google e pras IAs (SEO e GEO), com blog e rastreamento de anúncios, e texto que fala do problema do cliente. Nasce no seu computador e o /publicar-site coloca no ar."
   },
   {
    "c": "diagnostico-comunicacao",
    "d": "Descobre maneiras de produzir conteúdo que combinam com você e cabem na sua rotina, aproveitando o que já contou no chat. Sem cadastro extra."
   },
   {
    "c": "editar-video",
    "d": "Edita o vídeo que o advogado gravou no celular com um modelo do cardápio. Confere pausas e retomadas, põe legenda, gancho e animação, e devolve o MP4 para revisão."
   },
   {
    "c": "gerar-no-canva",
    "d": "Entrega a arte conferida em PNG pelo motor e, quando solicitado, cria uma cópia editável na conta Canva do advogado. O conector é opcional."
   },
   {
    "c": "google-meu-negocio",
    "d": "Cria, otimiza e mantém o Google Meu Negócio do advogado: o canal que faz o escritório aparecer quando alguém busca advogado perto de mim. A skill gera todo o conteúdo e guia cada clique; você só cola no painel, uns 2 minutos por rotina."
   },
   {
    "c": "mapear-personas",
    "d": "Mapeia as personas do público do advogado (até 4 perfis sustentados pelo material dele) com dores, objeções, linguagem e arquétipo FLG ideal. Vira a base de todo conteúdo gerado pela skill: reels, carrosséis, estáticos, artigos e calendário passam a mirar gente de verdade."
   },
   {
    "c": "meu-flg",
    "d": "Monta o FLG do advogado, o plano de crescimento do perfil dele no método do Samurai. Lê perfis públicos que ele admira (raspagem pela Apify, na conta dele, com o custo dito antes, ou por prints) e entrega em Word os pilares, o arquétipo, a matriz semanal e o roteiro de 90 dias."
   },
   {
    "c": "minha-marca",
    "d": "Configura nome, cores, assinatura, fotos e logo do advogado para vídeos, estáticos e carrosséis. Salva a preferência de modelo e as escolhas sobre avisos da OAB."
   },
   {
    "c": "modelar-video",
    "d": "Analisa as cenas de uma referência e propõe um roteiro próprio, com modelo de edição e tomadas para gravar no celular. Sem chave de API."
   },
   {
    "c": "modelos",
    "d": "Mostra opções visuais de carrossel, imagem única e vídeo, com prévias reais para escolher sem decorar comandos."
   },
   {
    "c": "nova-landing",
    "d": "Cria uma landing page de campanha: uma página, um problema, um botão de WhatsApp. É a página que recebe o anúncio (Meta, Google) e converte em conversa, falando do problema do cliente, não do advogado."
   },
   {
    "c": "novo-artigo",
    "d": "Gera artigo de blog jurídico com SEO + GEO embutidos, estrutura FLG e avisos específicos sobre OAB 205."
   },
   {
    "c": "novo-carrossel",
    "d": "Cria o texto e entrega o carrossel desenhado em PNG, com até 10 lâminas, na marca e no modelo escolhidos."
   },
   {
    "c": "novo-estatico",
    "d": "Produz a arte de uma imagem, em PNG, para feed 4:5, quadrado 1:1 ou story 9:16, usando o motor e a marca do advogado. Entrega também a legenda. O Canva é uma opção adicional."
   },
   {
    "c": "novo-reel",
    "d": "Gera roteiro de vídeo (reel 60s, stories 15s, vídeo longo 5min) com gancho, desenvolvimento e CTA."
   },
   {
    "c": "pesquisa-de-campanha",
    "d": "Pesquisa de mercado com dados públicos oficiais (Portal da Transparência, CAGED, SmartLab do MPT e IBGE, conforme disponibilidade e condições de uso verificadas) pra afiar a campanha da sua tese: descobre ONDE está o seu público, quantos são, como a dor aparece na região, e transforma isso em pra..."
   },
   {
    "c": "preparar-editor",
    "d": "Prepara o editor de vídeos e artes do MaestrIA Marketing neste computador, uma vez só. Mostra tudo o que vai baixar e pede licença antes; depois confere programa por programa e faz um vídeo de teste."
   },
   {
    "c": "publicar-artigo",
    "d": "Publica no blog do seu site um artigo gerado pelo /novo-artigo: monta a página do post com SEO e GEO, atualiza o índice do blog e, no modo plugado, republica o site na hora, direto da conversa."
   },
   {
    "c": "publicar-site",
    "d": "Coloca o site do advogado no ar, de graça, com o seu domínio e cadeado de segurança automático. Feito pra quem nunca mexeu com hospedagem: cada passo diz exatamente onde clicar."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "tom-de-voz",
    "d": "Constrói o Manual de Tom de Voz do advogado a partir de textos REAIS dele + entrevista guiada. Vira a voz de todo conteúdo gerado pela skill; reels, carrosséis, estáticos, artigos e calendário saem com a cara do advogado, não com cara de IA."
   },
   {
    "c": "video-pje",
    "d": "Prepara vídeo para juntar no PJe. Converte o vídeo do celular (inclusive iPhone e HDR) para MP4 comum e divide em partes abaixo do limite do tribunal, sem cortar nada. Entrega um LEIA-ME com o trecho e o código de conferência de cada parte, e uma sugestão de texto para a petição."
   }
  ]
 },
 "pensao-alimenticia": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Gera ação de alimentos, revisional, exoneração ou execução, conforme escolha."
   }
  ]
 },
 "plano-saude-cobertura": {
  "funcoes": [
   {
    "c": "nova-acao",
    "d": "Conduz intake e gera ação contra operadora de plano de saúde."
   }
  ]
 },
 "preparador-audiencia": {
  "funcoes": [
   {
    "c": "preparar",
    "d": "Prepara o advogado pra audiência. Gera roteiro de perguntas, checklist, posicionamento estratégico."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "sustentacao-oral",
    "d": "Monta o roteiro completo da sua sustentação oral em recurso (TRT, TRF, TJ ou turma recursal) a partir dos autos: tese central, os 2 ou 3 pontos que decidem o julgamento, respostas prontas pras perguntas prováveis dos julgadores e o texto cronometrado pro seu tempo de tribuna, entregue em Word."
   }
  ]
 },
 "quesitos-pericia": {
  "funcoes": [
   {
    "c": "gerar-quesitos",
    "d": "Gera lista de quesitos pra perícia médica, social, insalubridade ou engenharia."
   },
   {
    "c": "meus-peritos",
    "d": "Ficha do perito nomeado (o que ele costuma concluir, por região do corpo, onde e quando faz a perícia), alimentação da base de peritos da MaestrIA com leituras feitas com o login do próprio advogado, e a base do escritório com o relato de cada perícia."
   },
   {
    "c": "preparar-pericia",
    "d": "Gera o guia de preparação do CLIENTE pra perícia médica (INSS ou judicial) e pra avaliação social do BPC: o que será avaliado, documentos a levar, direitos do periciando. Em linguagem de leigo, entregue em Word pro advogado mandar. Orientação informativa; JAMAIS coaching de simulação."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "recurso-administrativo-inss": {
  "funcoes": [
   {
    "c": "novo-recurso",
    "d": "Conduz intake e gera recurso administrativo INSS em Word, atacando ponto a ponto o motivo do indeferimento."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   }
  ]
 },
 "revisional-bancaria": {
  "funcoes": [
   {
    "c": "alvara",
    "d": "Monta o pedido de expedição de alvará do que o banco depositou na revisional, no formato curto do escritório (alvará para a conta da sociedade, sem destaque) ou com alvarás separados se o advogado quiser, com a conta do repasse fora dos autos e a trava contra o extrato do depósito."
   },
   {
    "c": "cruzar-caso",
    "d": "Olha o caso pelas duas frentes do escritório, previdenciária e bancária, antes de decidir o que entrar."
   },
   {
    "c": "cumprimento-revisional",
    "d": "Monta o pedido de cumprimento de sentença da revisional a partir do dispositivo, com o demonstrativo do art. 524 e a multa e os honorários do art. 523, § 1º, do CPC."
   },
   {
    "c": "distribuir",
    "d": "Monta e confere o pacote de protocolo da revisional, documento a documento, antes de distribuir."
   },
   {
    "c": "notificar-banco",
    "d": "Gera a notificação extrajudicial que pede ao banco cópia dos contratos e extratos, e que sustenta a tutela de exibição depois."
   },
   {
    "c": "radar-juridico",
    "d": "Organiza decisões fornecidas pelo advogado em relatório local, com fontes, recorte regional, contagens auditáveis e revisão. Não estima chance individual."
   },
   {
    "c": "replica-bancaria",
    "d": "Monta a réplica à contestação do banco na revisional, tese a tese contra o mapa de defesas, com o cálculo refeito quando o banco junta o contrato."
   },
   {
    "c": "revisional",
    "d": "Monta a petição inicial da ação revisional de contrato bancário, no caminho com contrato ou no caminho sem contrato."
   }
  ]
 }
};
