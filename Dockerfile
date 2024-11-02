# Usa uma imagem base do Python
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do diretório atual para o diretório de trabalho no container
COPY . .

# Instala as dependências necessárias
RUN pip install --no-cache-dir flask Flask-Session flask-sqlalchemy werkzeug

# Expõe a porta que o Flask usará
EXPOSE 5000

# Define o comando padrão para rodar o aplicativo
CMD ["python", "app.py"]
