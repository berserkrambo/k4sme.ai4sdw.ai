FROM python:3.9.12

RUN pip install poetry
RUN mkdir /src
WORKDIR /src

COPY poetry.lock pyproject.toml /src/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi


COPY ai4sdw /src/ai4sdw

ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["uvicorn", "ai4sdw.main:app", "--host", "0.0.0.0", "--port", "8000"]
