FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5683 8000 8883

CMD ["sh", "-c","python mqtt_broker.py & python -m uvicorn app:app --host 0.0.0.0 --port 8000"]