# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /dvmn_check
COPY requirements.txt .env bot.py ./
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]