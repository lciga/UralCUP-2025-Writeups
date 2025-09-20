FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY server.py server.py
COPY web web
COPY flag.txt flag.txt
# RUN chmod +x /flag.txt

#RUN pyro4-ns -n 0.0.0.0 &
COPY startup.sh startup.sh
RUN chmod ugo+r flag.txt

CMD ["/bin/bash", "startup.sh"]
