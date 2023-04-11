FROM python:3.9

COPY ./app/requirements/ /opt/requirements/
RUN pip install -r /opt/requirements/docs.txt

COPY ./ /webserver

WORKDIR /webserver
