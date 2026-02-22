FROM nginx:stable-alpine

ENV TZ=America/Sao_Paulo

ARG ENV=prod

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/nanocalc.${ENV}.conf /etc/nginx/conf.d/nanocalc.conf
COPY conf.d/cloudflare_realip.conf /etc/nginx/conf.d/cloudflare_realip.conf

RUN mkdir -p /var/www/letsencrypt

EXPOSE 80
EXPOSE 443
