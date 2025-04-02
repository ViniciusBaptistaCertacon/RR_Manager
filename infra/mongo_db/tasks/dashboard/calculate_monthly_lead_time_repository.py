import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_monthly_lead_time(tasks_collection, start_date, end_date, creator=None):
    """
    Calcula o lead time médio (em dias) por mês, medindo a diferença entre
    gantt_bar_start_date e close_date, para as tarefas que foram finalizadas.

    Filtra as tarefas com base no período obrigatório (usando gantt_bar_start_date)
    e, opcionalmente, pelo criador (user_name).

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime): Data mínima para filtrar tarefas (aplicada em gantt_bar_start_date).
        end_date (datetime): Data máxima para filtrar tarefas (aplicada em gantt_bar_start_date).
        creator (str, opcional): Nome do criador para filtrar tarefas.

    Returns:
        list: Lista de dicionários com '_id' (mês, formato "YYYY-MM") e 'avg_lead_time' (em dias).
    """
    query = {
        "gantt_bar_start_date": {"$gte": start_date, "$lte": end_date},
        "close_date": {"$exists": True, "$ne": None},
        "gantt_bar_start_date": {"$exists": True, "$ne": None}
    }
    if creator:
        query["user_name"] = creator

    pipeline = [
        {"$match": query},
        {"$project": {
            "lead_time": {
                "$divide": [
                    {"$subtract": [
                        {"$toDate": "$close_date"},
                        {"$toDate": "$gantt_bar_start_date"}
                    ]},
                    86400000  # milissegundos em um dia
                ]
            },
            "month": {
                "$dateToString": {
                    "format": "%Y-%m",
                    "date": {"$toDate": "$gantt_bar_start_date"}
                }
            }
        }},
        {"$group": {
            "_id": "$month",
            "avg_lead_time": {"$avg": "$lead_time"}
        }},
        {"$sort": {"_id": 1}}
    ]

    logger.info("Executando agregação com pipeline: %s", pipeline)
    result = list(tasks_collection.aggregate(pipeline))
    return result
