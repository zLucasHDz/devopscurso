import logging
from datetime import datetime
import requests
from fastapi import FastAPI


# ================= LOGS =================

LOGGER = logging.getLogger("devops")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False

if not LOGGER.handlers:
    stream_handler = logging.StreamHandler()

    file_handler = logging.FileHandler(
        f"{LOGGER.name}.log",
        encoding="UTF-8"
    )

    formatador = logging.Formatter(
        fmt=(
            "%(name)s | %(levelname)s | %(asctime)s | "
            "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
        )
    )

    stream_handler.setFormatter(formatador)
    file_handler.setFormatter(formatador)

    LOGGER.addHandler(stream_handler)
    LOGGER.addHandler(file_handler)

# =============== FIM LOGS ===============


LISTA_TAREFAS = []
APP = FastAPI()


def nova_tarefa(id: int, titulo: str, descricao: str):
    """Cria uma nova tarefa usando um dicionário."""

    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }


def verificar_existencia_tarefa(id: int):
    """Verifica a existência de uma tarefa com base no ID."""

    for tarefa in LISTA_TAREFAS:
        if id == tarefa["id"]:
            return True

    return False


@APP.get("/")
def index():
    return "Olá, DevOps!"


@APP.get("/tarefas")
def listar_tarefas():
    """Lista o ID e o título das tarefas."""

    tarefas = []

    for tarefa in LISTA_TAREFAS:
        info = {
            "id": tarefa["id"],
            "titulo": tarefa["titulo"]
        }

        tarefas.append(info)

    return tarefas


@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    """Busca uma tarefa pelo seu ID."""

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            return tarefa

    LOGGER.warning("Tarefa não encontrada. ID: %s", id)

    return {"mensagem": "Não existe nenhuma tarefa com esse ID"}


@APP.post("/tarefas")
def criar_tarefa(id: int, titulo: str, descricao: str):
    """Cria uma nova tarefa."""

    if verificar_existencia_tarefa(id):
        LOGGER.warning("Tentativa de criar tarefa já existente. ID: %s", id)

        return {"mensagem": "TAREFA JÁ EXISTE!"}

    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    LOGGER.info("Tarefa criada. ID: %s", id)

    return {"mensagem": "OK"}


@APP.put("/tarefas/{id}")
def atualizar_tarefa(
    id: int,
    titulo: str = "",
    descricao: str = "",
    concluido: bool = False
):
    """Atualiza uma tarefa pelo seu ID."""

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] != id:
            continue

        if titulo != "":
            tarefa["titulo"] = titulo

        if descricao != "":
            tarefa["descricao"] = descricao

        tarefa["concluido"] = concluido

        if concluido:
            try:
                resposta = requests.post(
                    "http://notificacoes:8000/notificar",
                    params={
                        "titulo": tarefa["titulo"],
                        "data_finalizacao": datetime.now().isoformat()
                    },
                    timeout=10
                )

                resposta.raise_for_status()

                LOGGER.info(
                    "Notificação enviada para a tarefa. ID: %s",
                    id
                )

            except requests.RequestException as erro:
                LOGGER.error(
                    "Erro ao enviar notificação da tarefa ID %s: %s",
                    id,
                    erro
                )

        LOGGER.info("Tarefa atualizada. ID: %s", id)

        return {"mensagem": "OK"}

    LOGGER.warning("Tentativa de atualizar tarefa inexistente. ID: %s", id)

    return {"mensagem": "TAREFA NÃO EXISTE!"}


@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    """Remove uma tarefa pelo seu ID."""

    for indice, tarefa in enumerate(LISTA_TAREFAS):
        if tarefa["id"] == id:
            LISTA_TAREFAS.pop(indice)

            LOGGER.info("Tarefa apagada. ID: %s", id)

            return {"mensagem": "OK"}

    LOGGER.warning("Tentativa de apagar tarefa inexistente. ID: %s", id)

    return {"mensagem": "TAREFA NÃO EXISTE!"}