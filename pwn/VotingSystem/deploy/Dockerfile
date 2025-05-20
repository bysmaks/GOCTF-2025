FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

USER ctf
WORKDIR /home/ctf

COPY --chown=ctf:ctf pwn /home/ctf/pwn
COPY --chown=ctf:ctf flag.txt /home/ctf/flag.txt
COPY --chown=ctf:ctf ld-linux-x86-64.so.2 /home/ctf/lib/ld-linux-x86-64.so.2
COPY --chown=ctf:ctf libc.so.6 /home/ctf/lib/libc.so.6
COPY --chown=ctf:ctf run.sh /home/ctf/run.sh

EXPOSE 1773

CMD ["socat", "tcp-listen:1773,reuseaddr,fork", "exec:/home/ctf/run.sh"]

