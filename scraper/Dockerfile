FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
COPY app.py .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "-u", "app.py"]