# 1. Escolhe a imagem base (Python leve)
FROM python:3.13-slim AS poetry
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt 

# 3. Instala dependências do sistema necessárias para o PostgreSQL funcionar com Python
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# # 4. Copia o arquivo de dependências para o container
COPY --from=poetry /app/requirements.txt .

# 5. Instala as dependências Python no ambiente do container
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -c "import django; print(django.get_version())"

# 6. Copia o restante da aplicação Django
COPY . .

# 7. Expõe a porta padrão do Django
EXPOSE 8000

# 8. Comando para rodar o servidor da aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

