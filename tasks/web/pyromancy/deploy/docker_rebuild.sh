#!/bin/bash
sudo docker kill pyro
sudo docker rm pyro
sudo docker image rm test/test
sudo docker build . --tag test/test
sudo docker run -d -p 5643:9090 -p 5644:5644 -p 5645:5000 --name pyro test/test
