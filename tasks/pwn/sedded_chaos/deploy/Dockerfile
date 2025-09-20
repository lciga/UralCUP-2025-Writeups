FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y socat &&\
    useradd -m pwnuser

RUN mkdir /app
WORKDIR /app

COPY flag.txt /app
COPY chaos /app

USER pwnuser

EXPOSE 5013
CMD socat tcp-listen:5013,reuseaddr,fork exec:"./chaos"