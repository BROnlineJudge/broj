FROM python:latest

COPY . /var/pyej
WORKDIR /var/pyej
RUN pip install -r requirements.txt

EXPOSE 5432

CMD ["python", "./judge.py", "-l", "cpp"]
