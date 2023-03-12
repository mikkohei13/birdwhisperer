FROM python:3.10-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt update
RUN apt -y install ffmpeg

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN pip install -U openai-whisper

CMD ["tail", "-f", "/dev/null"]
