FROM nginx:1.15.12-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY blog.conf /etc/nginx/conf.d

RUN mkdir /etc/nginx/ssl
COPY ./ssl/* /etc/nginx/ssl/