FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python server.py & python attack.py & wait"]
