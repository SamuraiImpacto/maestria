FROM nginx:alpine

# Copia arquivos estáticos pra raiz do nginx
WORKDIR /usr/share/nginx/html
COPY *.html ./
COPY *.css ./
COPY *.js ./

# Área de membros (login por código de ativação + CPF, curso, chamados)
COPY membros/ ./membros/

# Landing pages segmentadas por área (campanhas de WhatsApp)
COPY prev/ ./prev/
COPY trab/ ./trab/

# Imagens (prints reais do guia de instalação)
COPY img/ ./img/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
