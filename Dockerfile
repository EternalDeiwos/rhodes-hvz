FROM python:2

RUN mkdir /app

COPY . /app

WORKDIR /app

EXPOSE 8080

ENV WORKERS 4
ENV WSGI_APP uchicagohvz.wsgi

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN pip install -r ./requirements.txt

CMD gunicorn --workers $WORKERS --access-logfile - --error-logfile - -b 0.0.0.0:8080 $WSGI_APP
