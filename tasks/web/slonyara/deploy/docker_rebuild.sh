#!/bin/bash
docker stop slon && docker rmi slon && \
docker build --tag=slon . && \
docker run -d -p 5059:80 --rm --name=slon -it slon
