FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# RUN pip install piper-tts

RUN python3 -m piper.download_voices en_US-lessac-medium

EXPOSE 5000

# CMD ["python3", "-m", "piper.http_server", "-m", "en_US-lessac-medium"]
