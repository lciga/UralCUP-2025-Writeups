FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# COPY flag.txt .
COPY config.py .
COPY templates templates
COPY app.py .

RUN export PYTHONDONTWRITEBYTECODE=1

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
# CMD ["python3", "app.py"]