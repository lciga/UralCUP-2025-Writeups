FROM ubuntu:22.04@sha256:4e0171b9275e12d375863f2b3ae9ce00a4c53ddda176bd55868df97ac6f21a6e

RUN apt-get update && \
    apt-get install -y socat &&\
    useradd -m pwnuser

RUN mkdir /app
WORKDIR /app

COPY flag.txt /app
COPY battle /app

USER pwnuser

EXPOSE 5012
CMD socat tcp-listen:5012,reuseaddr,fork exec:"./battle"