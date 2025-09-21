FROM php:8.2-apache

WORKDIR /var/www/html/

COPY . .
RUN bash -c 'FLAG_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12) && cp flag.txt "${FLAG_NAME}_flag.txt" && rm flag.txt'

RUN chown -R root:root /var/www/html \
    && chmod -R 755 /var/www/html

USER www-data

EXPOSE 80