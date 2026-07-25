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

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
