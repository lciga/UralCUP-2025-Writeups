#!/bin/bash
pyro4-ns -n 0.0.0.0 &
nohup python3 ./web/app.py > web.log 2>&1 &
python3 server.py

