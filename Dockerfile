# Imagem base leve com Python
FROM python:3.10-slim

# Instala bibliotecas do sistema necessárias para o rembg funcionar
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta que o Cloud Run usará
ENV PORT 8080
EXPOSE 8080

# Comando para iniciar o app usando Gunicorn, usando a variável PORT
CMD exec gunicorn --bind :$PORT app:app
