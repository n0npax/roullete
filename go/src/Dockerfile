FROM golang:latest as builder
LABEL maintainer=marcin.niemira@gmail.com

RUN mkdir /app
COPY  [^Dockerfile]* /app/
WORKDIR /app
RUN go install ./...

FROM debian:unstable-slim

RUN apt-get update
RUN apt-get install -y curl

COPY --from=builder /go/bin/* /usr/local/bin/
ENTRYPOINT ["sleep 300"]
