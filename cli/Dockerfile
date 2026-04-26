FROM golang:1.26-alpine@sha256:2389ebfa5b7f43eeafbd6be0c3700cc46690ef842ad962f6c5bd6be49ed82039 AS builder

WORKDIR /app
COPY ./ .

ARG TARGETARCH
RUN CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH} go build -ldflags="-s -w" -o aethersearch-cli .
RUN mkdir -p /home/aethersearch/.config

FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder --chown=65534:65534 /home/aethersearch /home/aethersearch

COPY --from=builder /app/aethersearch-cli /aethersearch-cli

ENV HOME=/home/aethersearch
ENV XDG_CONFIG_HOME=/home/aethersearch/.config

USER 65534:65534

ENTRYPOINT ["/aethersearch-cli"]
