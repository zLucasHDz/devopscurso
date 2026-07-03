from fastapi import FastAPI
from datetime import datetime

LISTA_TAREFAS = []
APP = FastAPI()

def nova_tarefa(id: int, titulo: str, descricao: str):
    """Função auxiliar para criar uma tarefa usando dicionário (`dict`)"""
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

@APP.get("/")
def index():
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():

    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []
    
    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    global LISTA_TAREFAS
    LISTA_TAREFAS.append(nova_tarefa(0, "nova tarefa", "descricao nova tarefa"))

    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}
    if len(LISTA_TAREFAS) == 0:
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao


@APP.post("/tarefas")
def recebe_tarefas(id: int, titulo: str, descricao: str):

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            return "TAREFA JÁ EXISTE"

    LISTA_TAREFAS.append(nova_tarefa(id, titulo, descricao))

    return "OK"

@APP.put("/tarefas/{id}")
def informa_tarefa(id: int, titulo: str, descricao: str, concluido: bool):

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            tarefa["titulo"] = titulo
            tarefa["descricao"] = descricao
            tarefa["concluido"] = concluido
            return "OK"

    return "TAREFA NÃO EXISTE"

@APP.delete("/tarefas/{id}")
def remover_tarefa(id: int):

    for tarefa in LISTA_TAREFAS:
        if tarefa["id"] == id:
            LISTA_TAREFAS.remove(tarefa)
            return "OK"

    return "TAREFA NÃO EXISTE"

        
        
# Implementar!
# @APP.post("/tarefas")
# Rota /tarefas (POST)
#   Entrada: id da tarefa (int), titulo da tarefa (str) e descrição da tarefa (str)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Cria uma nova tarefa usando a função `nova_tarefa`
#       - Adiciona nova tarefa a LISTA_TAREFAS
#   # Saída:
#       - Retorna "OK" se a tarefa foi criada
#       - Se a tarefa existir, retornar "TAREFA JÁ EXISTE"

# @APP.put("/tarefas/{id}")
# Rota /tarefas/{id} (PUT)
#   Entrada: id da tarefa (int), titulo da tarefa (str), descrição da tarefa (str) e concluido (bool)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Atualiza informações da tarefa de id específico
#   # Saída:
#       - Retorna "OK" se a tarefa foi atualizada
#       - Se a tarefa NÃO existir, retornar "TAREFA NÃO EXISTE"

# @APP.delete("/tarefas")
# Rota /tarefas/{id} (DELETE)
#   Entrada: id da tarefa (int)
#   Funcionamento:
#       - Recebe os dados como parâmetro de requisição
#       - Busca pela tarefa com base no ID
#       - Se tarefa existir, remover de LISTA_TAREFAS
#       - Se NÃO existir, retorna "TAREFA NÃO EXISTE"
#   # Saída:
#       - Retorna "OK" se a tarefa foi removida
#       - Se a tarefa NÃO existir, retornar "TAREFA NÃO EXISTE"