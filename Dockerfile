FROM python:3.12-alpine3.19

ARG TARGETARCH

COPY mdocker /opt/mdocker
COPY pyproject.toml /opt
COPY poetry.lock /opt
COPY tests /opt/tests
COPY README.md /opt
COPY LICENSE.md /opt

ENV PYTHONPATH /opt
WORKDIR /opt

# cffi wheel in Python dependencies needs to be built manually for arm64
RUN if [ "${TARGETARCH}" == "arm64" ]; then \
    apk update && apk add gcc musl-dev libffi-dev; fi

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install poetry twine && \
    python3 -m poetry config virtualenvs.create false && \
    python3 -m poetry install --no-root && \
    python3 -m pytest tests/

CMD [ "/bin/sh" ]
