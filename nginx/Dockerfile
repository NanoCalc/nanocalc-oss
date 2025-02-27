FROM nginx:stable-alpine

# By default, NGINX Docker image runs as user "nginx" which has 101 as both UID and GID  
ARG ENV=prod
COPY conf.d/nanocalc.${ENV}.conf /etc/nginx/conf.d/nanocalc.conf

EXPOSE 80
EXPOSE 443
