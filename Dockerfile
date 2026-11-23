FROM nginx:alpine

# Copia arquivos estáticos pra raiz do nginx
WORKDIR /usr/share/nginx/html
COPY *.html ./
COPY *.css ./
COPY *.js ./

# Preparador automático do PC (o manual de instalação manda baixar)
COPY *.ps1 ./

# Preparador de 1 clique (instala Git + Python via winget antes do Claude Code)
COPY *.bat ./

# Guia oficial do instalador (verificação de autenticidade pelo Claude do cliente)
COPY *.txt ./

# Área de membros (login por código de ativação + CPF, curso, chamados)
COPY membros/ ./membros/

# Landing pages segmentadas por área (campanhas de WhatsApp)
COPY prev/ ./prev/
COPY trab/ ./trab/
COPY marketing/ ./marketing/
# Combo Previdenciário + Marketing (checkout urkdMlQ), para mandar a quem já usa o Claude.
COPY prev-marketing/ ./prev-marketing/
# Combo Trabalhista + Marketing (checkout 3J6V58l).
COPY trab-marketing/ ./trab-marketing/

# Black do MaestrIA Marketing (pagina de oferta).
# ⛔ ESTE ARQUIVO E A LISTA DE QUEM SOBE. Pasta nova no repositorio NAO vai
#    para o ar sozinha: ela precisa de um COPY aqui. Sem isso o deploy passa
#    verde, o commit certo aparece no historico do EasyPanel, e a pasta
#    simplesmente nao existe no servidor. Foi o que aconteceu com a /black/
#    em 22/10/2026: uma tarde de caca a um 404 que era uma linha faltando.
COPY black/ ./black/

# Redirect do endereço antigo do diagnóstico (/diagnostico -> /prev/diagnostico).
# O funil em si mora dentro de prev/, então já sobe no COPY prev/ lá em cima.
COPY diagnostico/ ./diagnostico/

# Proposta de consultoria (Samurai Lab) para o Jardson
COPY jardson/ ./jardson/

# Imagens (prints reais do guia de instalação)
COPY img/ ./img/

# Meta Pixel (arquivo único carregado por todas as páginas públicas).
# Sem este COPY o /js/pixel.js dá 404 e o pixel não dispara em lugar nenhum,
# mesmo com a tag presente no HTML.
COPY js/ ./js/

# As duas vitrines de modelos, linkadas pelo card das LPs.
# ⛔ ESTE ARQUIVO E A LISTA DE QUEM SOBE: pasta nova no repositorio NAO vai para o
#    ar sozinha, precisa de um COPY aqui. Foi o que segurou a /black/ em 22/10.
COPY modelos/ ./modelos/
COPY modelos-video/ ./modelos-video/

# Funil do perfil Samurai do Jurídico: pack grátis (/prompts/) e venda do kit de R$ 47 (/kit/).
# Geradas por C:/Acervo/Iscas/MaestrIA-2026-11/paginas_funil.py a partir dos .md testados.
COPY prompts/ ./prompts/
COPY kit/ ./kit/
# Low ticket de R$ 67 (365 roteiros): venda, começar e entrega. Geradas por paginas_reels.py.
COPY reels/ ./reels/
# Áreas lançadas em 07/11/2026 e a página do Full: cada pasta nova precisa do seu COPY.
COPY familia/ ./familia/
COPY criminal/ ./criminal/
COPY imobiliario/ ./imobiliario/
COPY consumidor/ ./consumidor/
COPY empresarial/ ./empresarial/
COPY bancario/ ./bancario/
COPY full/ ./full/
# Página da aula ao vivo de 11/11/2026 (QR code dos slides): tudo o que a MaestrIA faz e os links.
COPY aula/ ./aula/
# Lista de espera da Implementação de IA (14/11/2026): formulário que grava pela edge lista-espera.
COPY lista-de-espera/ ./lista-de-espera/
# Teste grátis de 7 dias (20/11/2026): página de entrada do teste.
COPY teste/ ./teste/
# Raio-X da marca do advogado (21/11/2026): diagnóstico que grava pela edge raio-x-marca.
COPY raio-x/ ./raio-x/
# Consultoria de tráfego com o Samurai (22/11/2026): formulário que grava pela edge consultoria-trafego.
COPY consultoria/ ./consultoria/
# Maratona de Lives do Samurai (21/11/2026): convite, agenda, arte e legenda. Grava pela edge lives-maratona.
COPY lives/ ./lives/
COPY cohort/ ./cohort/

# O navegador guardava a página antiga e o Samurai via versão velha (22/11/2026).
# Manda o navegador conferir com o servidor a cada visita; se nada mudou, a resposta é curta (304).
# Endereço sem barra no fim (/cohort) redireciona relativo, sem cair em http.
RUN printf 'add_header Cache-Control "no-cache" always;\nabsolute_redirect off;\n' > /etc/nginx/conf.d/00-sem-pagina-velha.conf && nginx -t

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
