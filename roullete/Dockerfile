FROM golang:latest as builder
LABEL maintainer=marcin.niemira@gmail.com
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN go install ./...

FROM alpine:latest
COPY --from=builder /go/bin/* /usr/local/bin

