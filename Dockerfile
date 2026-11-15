
FROM python:3.13-slim AS poetry
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt 


FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY --from=poetry /app/requirements.txt .


RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -c "import django; print(django.get_version())"


COPY . .


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

