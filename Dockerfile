FROM python:3.10

RUN apt-get update && apt-get -y upgrade

WORKDIR /app

RUN pip install -U pip
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY . /app
RUN ~/.local/share/pypoetry/venv/bin/poetry update
RUN ~/.local/share/pypoetry/venv/bin/poetry export --dev -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80