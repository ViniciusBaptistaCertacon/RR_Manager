import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def count_tasks_by_status(tasks_collection, start_date=None, end_date=None, creator=None):
    """
    Conta as tarefas por status (board_stage_name) na coleção do MongoDB,
    aplicando filtros opcionais para período (start_date e end_date) e criador (creator).

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime, opcional): Data de início para filtrar tarefas.
        end_date (datetime, opcional): Data de fim para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        list: Lista de dicionários com '_id' representando o status e 'count' com a contagem.
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
        {"$group": {"_id": "$board_stage_name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]

    logger.info("Executando agregação com pipeline: %s", pipeline)
    result = list(tasks_collection.aggregate(pipeline))
    return result