from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from datetime import datetime

import requests
import logging

LISTA_TAREFAS = []
APP = FastAPI()
LOGGER = logging.getLogger("DevOps")
LOGGER.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
file_handler   = logging.FileHandler("api.log", encoding='utf-8')
fmt = logging.Formatter(fmt="%(name)s | %(asctime)s | %(filename)s:%(lineno)s | %(levelname)s | %(message)s")

stream_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)

LOGGER.addHandler(stream_handler)
LOGGER.addHandler(file_handler)

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    tarefa = {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

    LOGGER.debug(f"Criando tarefa='{tarefa}'")

    return tarefa

def verificar_existencia_tarefa(id: int):
    """Função auxiliar para verificar a existência de uma tarefa com base no seu ID"""
    for tarefa in LISTA_TAREFAS:
        if id == tarefa['id']:
            return True
    return False

@APP.get("/")
def index():
    LOGGER.info(f"Rota '/' foi acessada")
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    # Lista tarefas (somente id e titulo)
    
    LOGGER.info(f"Rota '/tarefas' foi acessada")

    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []
    
    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}
    if len(LISTA_TAREFAS) == 0:
        LOGGER.error(f"Rota '/tarefas/{id} acessada. Mensagem: {mensagem_padrao['mensagem']}")
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        LOGGER.info(f"Rota '/tarefas/{id} acessada.")
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao

@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if tarefa_existe:
        ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
        LOGGER.error(f"Rota POST '/tarefas/' acessada. Tarefa já existe.")
        raise ex
    
    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    LOGGER.info(f"Rota POST '/tarefas' acessada. Tarefa id={id} criada.")

    return {"mensagem": "OK"}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        LOGGER.error(f"Rota PUT '/tarefas/{id}' acessada. Tarefa NÃO existe.")
        return {"mensagem": "TAREFA NÃO EXISTE!"}
    
    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    if titulo != "":
        LISTA_TAREFAS[indice]['titulo'] = titulo
    
    if descricao !=  "":
        LISTA_TAREFAS[indice]['descricao'] = descricao
    
    if concluido == True:
        requests.post(
            f"http://notificacoes:8000/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}",
            timeout=10
        )

    LISTA_TAREFAS[indice]['concluido'] = concluido
    LOGGER.debug(f"Tarefa atualizada = {LISTA_TAREFAS[indice]}")
    LOGGER.info(f"Rota PUT '/tarefas/{id}' acessada. Tarefa id={id} atualizada.")

    return {"mensagem": "OK"}

@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        LOGGER.error(f"Rota PUT '/tarefas/{id}' acessada. Tarefa NÃO existe.")
        return {"mensagem": "TAREFA NÃO EXISTE"}

    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    LISTA_TAREFAS.pop(indice)

    LOGGER.info(f"Rota DELETE '/tarefas/{id}' acessada. Tarefa id={id} removida.")

    return {"mensagem": "OK"}