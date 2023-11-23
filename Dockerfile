FROM python:3.12.0-alpine3.18

COPY mdocker /opt/mdocker
COPY pyproject.toml /opt
COPY poetry.lock /opt
COPY tests /opt/tests
COPY README.md /opt

ENV PYTHONPATH /opt
WORKDIR /opt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install poetry twine && \
    python3 -m poetry config virtualenvs.create false && \
    python3 -m poetry install --no-root && \
    python3 -m pytest tests/

CMD [ "/bin/bash" ]
