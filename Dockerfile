FROM python:2

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN pip install -r ./requirements.txt
RUN python manage.py syncdb --noinput

CMD ["python", "manage.py", "0.0.0.0:80"]
