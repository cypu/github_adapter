FROM ubuntu:latest
MAINTAINER Piotr Szczepanski

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /github_adapter
WORKDIR /github_adapter
RUN pip3 install -r requirements.txt

CMD ["python3", "run.py"]