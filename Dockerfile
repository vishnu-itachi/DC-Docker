FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3.9

WORKDIR /root/

# COPY src/* ./src/

ENTRYPOINT ./src/run.sh
