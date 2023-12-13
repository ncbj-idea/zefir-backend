FROM alpine:3.14 as base

WORKDIR /code
COPY . .   
RUN apk --no-cache add gettext=~0.21
# hadolint ignore=SC2016
RUN source .bash; envsubst '${API_PORT}' < nginx.conf-template > /etc/nginx.conf
RUN dos2unix /etc/nginx.conf
FROM nginx:stable
RUN rm /etc/nginx/nginx.conf
COPY --from=base /etc/nginx.conf /etc/nginx/nginx.conf
