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

# Copia os arquivos do projeto para dentro da imagem
COPY . .

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta que o Render usará
EXPOSE 5000

# Comando para iniciar o app usando Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
