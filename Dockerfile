FROM python:2

RUN mkdir /app
RUN mkdir /config

COPY ./requirements.txt /config/requirements.txt
VOLUME /app

EXPOSE 8080

ENV WORKERS 4
ENV WSGI_APP uchicagohvz.wsgi

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev nodejs -y

WORKDIR /app
RUN pip install -r /config/requirements.txt

CMD gunicorn --workers $WORKERS --access-logfile - --error-logfile - -b 0.0.0.0:8080 $WSGI_APP
