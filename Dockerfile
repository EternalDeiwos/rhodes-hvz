FROM python:2

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev python-psycopg2
RUN pip install -r ./requirements.txt
RUN python manage.py syncdb --noinput
RUN python manage.py schemamigration users --initial
RUN python manage.py schemamigration game --initial
RUN python manage.py migrate users
RUN python manage.py migrate game

CMD ["python", "manage.py", "0.0.0.0:80"]
