FROM python:3.9-slim-buster

RUN mkdir /bot && chmod +rwx /bot
COPY requirements.txt /bot/requirements.txt
# COPY bot /bot/bot
COPY run.sh /bot/run.sh

WORKDIR /bot

RUN chmod +x /bot/run.sh && \
    apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get -y install bash netcat && \
    pip install -r requirements.txt

CMD ./run.sh