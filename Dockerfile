FROM python:3.14-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY main.py weather_data.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
