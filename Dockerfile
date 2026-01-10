FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc netcat-openbsd postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./metro /app/
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "metro.wsgi:application", "--bind", "0.0.0.0:8000"]

