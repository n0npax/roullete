FROM python:latest
LABEL maintainer=marcin.niemira@gmail.com

RUN mkdir /app
COPY  ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh -c 'sleep 300'"]
