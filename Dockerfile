FROM python:3.12.2-slim
EXPOSE 80

# Setup user
ENV UID=2000
ENV GID=2000
ENV POETRY_VERSION=1.8.2

RUN groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init --shell /bin/bash -u "${UID}" -g "${GID}" python

USER python
WORKDIR /home/python

RUN pip install poetry
RUN pip install gunicorn
COPY ./poetry.lock ./pyproject.toml ./
COPY ./app ./app
ENV PYTHONPATH="/home/python"
RUN /home/python/.local/bin/poetry install --no-root

CMD ["/home/python/.local/bin/poetry", "run", "python", "app/main.py"]
