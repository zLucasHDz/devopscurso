FROM python:3.12-slim

RUN mkdir app/

WORKDIR app/

COPY requiriments.txt .
COPY app/main.py .
COPY app/notificacao.py .

RUN pip install -r requiriments.txt

ENTRYPOINT ["fastapi", "run"]

#Construir imagem Docker(docker build)
#Executar container com base na imagem (mapear porta 8000 do container para 80 do host)
#Tornar a porta 80 como pública
#Acessar página do navegador para testar