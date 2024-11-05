FROM python:3.11.5-slim

RUN mkdir /fastapi_training_user

WORKDIR /fastapi_training_user

COPY pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD ["uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]