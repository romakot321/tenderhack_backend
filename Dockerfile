FROM python:3.12.2-slim
EXPOSE 80

# Setup user
ENV UID=2000
ENV GID=2000

RUN groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init --shell /bin/bash -u "${UID}" -g "${GID}" python

USER python
WORKDIR /home/python

RUN pip3 install "poetry-core" "poetry==${POETRY_VERSION}"
COPY ./poetry.lock ./pyproject.toml .
COPY ./app ./app
RUN poetry install --no-root


CMD gunicorn app.main:fastapi_app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
