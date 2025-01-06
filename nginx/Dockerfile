FROM nginx:stable-alpine

ARG ENV=prod
COPY conf.d/nanocalc.${ENV}.conf /etc/nginx/conf.d/nanocalc.conf

EXPOSE 80
EXPOSE 443
