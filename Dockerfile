FROM gcc:latest
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python-pip

RUN apt-get install -y vim

RUN pip install pika
COPY . /var/pyej
WORKDIR /var/pyej

# CMD ["python3 judge.py"]
