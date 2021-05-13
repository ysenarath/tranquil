FROM ubuntu:16.04

LABEL maintainer="ysenarath.93@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /tweeflow/requirements.txt

WORKDIR /tweeflow

RUN pip install -r requirements.txt

COPY . /tweeflow

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]