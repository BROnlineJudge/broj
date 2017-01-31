FROM python:latest

RUN pip install pika

COPY . /var/pyej
WORKDIR /var/pyej

CMD ["python", "./judge.py", "-b", "*.*.*"]
