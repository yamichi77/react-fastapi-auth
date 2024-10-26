FROM python:3.11-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

ENTRYPOINT ["/src/start.sh"]
