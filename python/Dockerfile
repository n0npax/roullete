FROM python:latest
LABEL maintainer=marcin.niemira@gmail.com

COPY ./app/requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir /app
COPY  ./app /app
WORKDIR /app

ENTRYPOINT ["sh -c 'sleep 300'"]
