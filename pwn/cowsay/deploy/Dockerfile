FROM ubuntu:24.04

RUN apt-get -y update
RUN apt-get -y install socat

RUN useradd -m ctf

USER ctf
WORKDIR /home/ctf
COPY cowsay  /home/ctf
COPY flag  /home/ctf
EXPOSE 1777
CMD socat tcp-listen:1773,reuseaddr,fork exec:"./cowsay"
