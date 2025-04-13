FROM python:3.11-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y \
        gcc \
        tesseract-ocr \
        poppler-utils \
        build-essential \
        curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
