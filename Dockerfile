# Use a imagem oficial do Python para o FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copie o código da aplicação para o diretório /app no contêiner
COPY ./app /app

# Instale as dependências do seu projeto
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exponha a porta 8000 para permitir o acesso ao aplicativo
EXPOSE 8000

# Comando para iniciar o aplicativo FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]