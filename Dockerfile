FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry lock --no-update
RUN poetry install

COPY . /app/

CMD [ "uvicorn",  "app.main:app","--host","0.0.0.0","--port","8000","--reload"]
