import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_estimated_lead_time_by_month(tasks_collection, start_date: datetime = None, end_date: datetime = None):
    """
    Calcula o lead time estimado (diferença entre desired_start_date e desired_date_with_time)
    agrupado por mês, convertendo o average_lead_time para horas.

    Filtra apenas as tarefas que possuem valores válidos em desired_start_date e desired_date_with_time.
    Se desired_date_with_time estiver vazio, a tarefa está em andamento e é desconsiderada.

    Permite filtros de período baseados em desired_start_date.

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime, opcional): Data mínima para o filtro.
        end_date (datetime, opcional): Data máxima para o filtro.

    Returns:
        list: Lista de dicionários com:
              - _id: mês (formato "YYYY-MM")
              - average_lead_time: média do lead time estimado (em horas)
              - total_lead_time: soma total dos lead times (em horas)
              - count: quantidade de tarefas consideradas
    """
    query = {
        "desired_start_date": {"$exists": True, "$ne": None},
        "desired_date_with_time": {"$exists": True, "$ne": None}
    }
    if start_date:
        query["desired_start_date"]["$gte"] = start_date.isoformat()
    if end_date:
        query["desired_start_date"]["$lte"] = end_date.isoformat()

    pipeline = [
        {"$match": query},
        {"$project": {
            "month": {
                "$dateToString": {"format": "%Y-%m", "date": {"$toDate": "$desired_start_date"}}
            },
            "lead_time": {
                "$subtract": [
                    {"$toDate": "$desired_date_with_time"},
                    {"$toDate": "$desired_start_date"}
                ]
            }
        }},
        {"$group": {
            "_id": "$month",
            "average_lead_time": {"$avg": "$lead_time"},
            "total_lead_time": {"$sum": "$lead_time"},
            "count": {"$sum": 1}
        }},
        {"$project": {
            "_id": 1,
            "average_lead_time": {"$divide": ["$average_lead_time", 86400000]},
            "total_lead_time": {"$divide": ["$total_lead_time", 86400000]},
            "count": 1
        }},
        {"$sort": {"_id": 1}}
    ]

    result = list(tasks_collection.aggregate(pipeline))
    return result
