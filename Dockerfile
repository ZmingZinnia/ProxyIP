From ubuntu:20.04

ENV CODEDIR=/opt/code VENVDIR=/opt/venv

EXPOSE 3289

WORKDIR "${CODEDIR}"

COPY . "${CODEDIR}"

RUN apt-get update 
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime & apt-get install python3 curl python3-pip libxml2-dev libxslt1-dev python3-dev gcc musl-dev g++ -y

RUN pip3 install -r "${CODEDIR}/requirements.txt"

ENTRYPOINT ["python3", "client.py"]
