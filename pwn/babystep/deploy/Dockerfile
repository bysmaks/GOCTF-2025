FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

USER ctf
WORKDIR /home/ctf

COPY --chown=ctf:ctf baby /home/ctf/baby
COPY --chown=ctf:ctf flag.txt /home/ctf/flag.txt

EXPOSE 1774

CMD ["socat", "tcp-listen:1774,reuseaddr,fork", "exec:./baby"]
