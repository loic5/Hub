FROM python:3.8-slim

RUN apt-get -y update && \
    apt-get -y install git wget build-essential python-setuptools python3-dev libjpeg-dev libpng-dev zlib1g-dev && \
    apt install build-essential

RUN mkdir /app

RUN git clone https://github.com/activeloopai/Hub.git /app/ && \
    cd /app/

WORKDIR /app

ENV PYTHONPATH="/app/Hub:$PYTHONPATH"
RUN ls hub/
RUN pip install -r hub/requirements/requirements.txt && \
    pip install -r hub/requirements/common.txt && \
    pip install -r hub/requirements/tests.txt && \
    pip install -r hub/requirements/plugins.txt

