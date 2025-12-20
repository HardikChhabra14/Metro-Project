FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "metro.wsgi:application", "--bind", "0.0.0.0:8000"]

