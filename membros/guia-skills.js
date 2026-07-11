// Gerado automaticamente a partir dos comandos reais das skills (nao editar a mao).
// Regenerar: manutencao/pipeline-lote/gerar_guia.py
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
    "d": "Busca jurisprudência sobre um tema específico, VALIDA cada acórdão candidato em fonte oficial (DataJud CNJ + site do tribunal), e devolve só os validados. JAMAIS cita jurisprudência inventada."
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
    "c": "nova-peticao",
    "d": "Gera uma nova petição. Conduz intake guiado por tipo de peça, recebe prints, gera Word com formatação do modelo do escritório, salva local na pasta do caso."
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
   }
  ]
 },
 "auditor-previdenciario": {
  "funcoes": [
   {
    "c": "auditar",
    "d": "Audita o CNIS do segurado vs documentos. Detecta gaps, indicadores e sugere ações de correção."
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
    "c": "resumir-processo",
    "d": "Recebe os autos de um processo em andamento (PDF, mesmo grandão) e devolve a ficha executiva: partes, linha do tempo das decisões, estado atual, prazos em risco e próximos passos. O comando de quem pegou o caso pela metade."
   },
   {
    "c": "triagem-caso",
    "d": "Triagem do PRIMEIRO contato do cliente: joga a conversa de WhatsApp (texto ou áudio) e recebe: área do direito, urgência com alerta de prazo e prescrição, viabilidade preliminar, documentos a pedir e minuta de resposta pronta. O SDR jurídico rodando na sua máquina."
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
    "c": "jurimetria",
    "d": "Jurimetria 2.0 com dado oficial do CNJ (DataJud), grátis. Taxa real de procedência por vara, taxa de acordo, tempo mediano até sentença, tendência ano a ano e comparação entre tribunais. Responde onde ajuizar e como aquele juízo se comporta. Não tem nome de parte, juiz nem perito."
   },
   {
    "c": "planejamento-previdenciario",
    "d": "Planejamento previdenciário completo pra vender como consultoria. Projeta ano a ano quando cada regra de aposentadoria destrava, compara aposentar agora vs esperar, simula estratégias de contribuição (teto, plano simplificado, parar de contribuir) com custo-benefício, e entrega relatório em Word ..."
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
    "d": "Jurimetria 2.0 com dado oficial do CNJ (DataJud), grátis. Taxa real de procedência por vara, taxa de acordo, tempo mediano até sentença, tendência ano a ano e comparação entre tribunais. Responde onde ajuizar e como aquele juízo se comporta. Não tem nome de parte, juiz nem perito."
   }
  ]
 },
 "contestacao-trabalhista": {
  "funcoes": [
   {
    "c": "nova-contestacao",
    "d": "Conduz intake e gera contestação trabalhista atacando ponto a ponto cada pedido da inicial."
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
   }
  ]
 },
 "impugnacao-ppp": {
  "funcoes": [
   {
    "c": "impugnar-ppp",
    "d": "Gera impugnação técnica ao PPP defeituoso, atacando os 8 vícios mais comuns."
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
    "c": "calendario-editorial",
    "d": "Gera calendário editorial mensal (30 dias) com tema, formato e pilar FLG por dia."
   },
   {
    "c": "criar-site",
    "d": "Constrói o site profissional completo do advogado: rápido, preparado pro Google e pras IAs (SEO e GEO), com blog e rastreamento de anúncios, e texto que fala do problema do cliente. Nasce no seu computador e sobe de graça pro ar (o /publicar-site cuida da publicação)."
   },
   {
    "c": "gerar-no-canva",
    "d": "Gera a arte de um conteúdo (estático, carrossel, capa de reel) direto no Canva do advogado, usando o conector oficial do Canva. Se o Canva não estiver conectado, guia a conexão em 2 minutos ou entrega a direção de arte pra montagem manual."
   },
   {
    "c": "google-meu-negocio",
    "d": "Cria, otimiza e mantém o Google Meu Negócio do advogado: o canal que faz o escritório aparecer quando alguém busca advogado perto de mim. A skill gera todo o conteúdo e guia cada clique; você só cola no painel, uns 2 minutos por rotina."
   },
   {
    "c": "mapear-personas",
    "d": "Mapeia as personas do público do advogado (2 a 4 perfis) com dores, objeções, linguagem e arquétipo FLG ideal. Vira a base de todo conteúdo gerado pela skill: reels, carrosséis, estáticos, artigos e calendário passam a mirar gente de verdade."
   },
   {
    "c": "nova-landing",
    "d": "Cria uma landing page de campanha: uma página, um problema, um botão de WhatsApp. É a página que recebe o anúncio (Meta, Google) e converte em conversa, falando do problema do cliente, não do advogado."
   },
   {
    "c": "novo-artigo",
    "d": "Gera artigo de blog jurídico com SEO + GEO embutidos, filtros FLG e blindagem OAB 205."
   },
   {
    "c": "novo-carrossel",
    "d": "Gera carrossel Instagram (8-12 slides) com lógica de leitura forte."
   },
   {
    "c": "novo-estatico",
    "d": "Gera post estático de feed (imagem única): headline, copy, legenda completa e direção de arte pronta pra montar no Canva (ou gerar direto via /gerar-no-canva). Estrutura FLG + filtro OAB 205 automático."
   },
   {
    "c": "novo-reel",
    "d": "Gera roteiro de vídeo (reel 60s, stories 15s, vídeo longo 5min) com gancho, desenvolvimento e CTA."
   },
   {
    "c": "pesquisa-de-campanha",
    "d": "Pesquisa de mercado com dados públicos oficiais (Portal da Transparência, CAGED, SmartLab do MPT, IBGE, DataJud) pra afiar a campanha da sua tese: descobre ONDE está o seu público, quantos são, como a dor aparece na região, e transforma isso em praças, ângulos de criativo e plano de segmentação."
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
    "c": "tom-de-voz",
    "d": "Constrói o Manual de Tom de Voz do advogado a partir de textos REAIS dele + entrevista guiada. Vira a voz de todo conteúdo gerado pela skill; reels, carrosséis, estáticos, artigos e calendário saem com a cara do advogado, não com cara de IA."
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
    "c": "preparar-pericia",
    "d": "Gera o guia de preparação do CLIENTE pra perícia médica (INSS ou judicial) e pra avaliação social do BPC: o que será avaliado, documentos a levar, direitos do periciando. Em linguagem de leigo, entregue em Word pro advogado mandar. Orientação informativa; JAMAIS coaching de simulação."
   }
  ]
 },
 "recurso-administrativo-inss": {
  "funcoes": [
   {
    "c": "novo-recurso",
    "d": "Conduz intake e gera recurso administrativo INSS em Word, atacando ponto a ponto o motivo do indeferimento."
   }
  ]
 }
};
