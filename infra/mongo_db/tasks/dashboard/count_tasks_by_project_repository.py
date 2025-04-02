import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def count_tasks_by_project(tasks_collection, start_date=None, end_date=None, creator=None):
    """
    Conta as tarefas por projeto utilizando o campo custom_259 (label do projeto) na coleção do MongoDB,
    aplicando filtros opcionais para período (start_date e end_date) e criador (creator).
    Quando o campo do projeto não existir, agrupa como "sem_projeto".

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime, opcional): Data de início para filtrar tarefas.
        end_date (datetime, opcional): Data de fim para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        list: Lista de dicionários com '_id' representando o projeto e 'count' com a quantidade de tarefas.
    """
    query = {}
    if start_date or end_date:
        query["created_at"] = {}
        if start_date:
            query["created_at"]["$gte"] = start_date
        if end_date:
            query["created_at"]["$lte"] = end_date
    if creator:
        query["user_name"] = creator

    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": {"$ifNull": ["$custom_fields.custom_259.label", "SEM PROJETO"]},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]

    logger.info("Executando agregação com pipeline: %s", pipeline)
    result = list(tasks_collection.aggregate(pipeline))
    return result
