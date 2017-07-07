FROM python:2

RUN mkdir /app

COPY . /app

WORKDIR /app

EXPOSE 6379

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN pip install -r ./requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
