FROM nginx:stable-bookworm-perl

RUN apt update -y && apt install iptables -y

COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /
RUN chmod 0770 /entrypoint.sh

ENTRYPOINT "/entrypoint.sh"
