FROM python:2

RUN mkdir /app

VOLUME /app

WORKDIR /app

EXPOSE 6379, 8080

ENV WORKERS 4

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev gunicorn -y
RUN pip install -r ./requirements.txt

CMD ["gunicorn", "--workers", "$WORKERS", "-n", "gunicorn_hvz", "-b", "0.0.0.0:8080", "uchicagohvz:wsgi"]
