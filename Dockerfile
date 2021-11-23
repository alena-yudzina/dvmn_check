# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /dvmn_check

ENV BOT_TOKEN=""
ENV CHAT_ID=""
ENV DVMN_TOKEN=""
ENV LOG_BOT_TOKEN=""

RUN pip install -U pip python-dotenv requests python-telegram-bot
COPY bot.py ./

ENTRYPOINT ["python", "bot.py"]