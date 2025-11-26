FROM python:3.11

RUN apt-get update && apt-get install -y ansible ansible-lint

copy requirements.yml .

RUN ansible-galaxy collection install -r requirements.yml

RUN pip install  pyvmomi

USER root
