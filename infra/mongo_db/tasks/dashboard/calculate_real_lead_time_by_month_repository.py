import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_real_lead_time_by_month(tasks_collection, start_date: datetime = None, end_date: datetime = None):
    """
    Calcula o lead time real (diferença entre start_date e close_date) agrupado por mês,
    convertendo o average_lead_time para horas.

    Filtra apenas as tarefas que possuem valores válidos em start_date e close_date.
    Se close_date estiver vazio, a tarefa está em andamento e é desconsiderada.

    Permite filtros de período baseados em start_date.

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime, opcional): Data mínima para o filtro.
        end_date (datetime, opcional): Data máxima para o filtro.

    Returns:
        list: Lista de dicionários com:
              - _id: mês (formato "YYYY-MM")
              - average_lead_time: média do lead time (em horas)
              - total_lead_time: soma total dos lead times (em horas)
              - count: quantidade de tarefas consideradas
    """
    query = {
        "start_date": {"$exists": True, "$ne": None},
        "close_date": {"$exists": True, "$ne": None}
    }
    if start_date:
        query["start_date"]["$gte"] = start_date.isoformat()
    if end_date:
        query["start_date"]["$lte"] = end_date.isoformat()

    pipeline = [
        {"$match": query},
        {"$project": {
            "month": {
                "$dateToString": {"format": "%Y-%m", "date": {"$toDate": "$start_date"}}
            },
            "lead_time": {
                "$subtract": [
                    {"$toDate": "$close_date"},
                    {"$toDate": "$start_date"}
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
