from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard import calculate_monthly_lead_time


def get_monthly_lead_time(start_date, end_date, creator=None):
    """
    Retorna, para o período informado (aplicado sobre gantt_bar_start_date), a média do lead time por mês.

    Args:
        start_date (datetime): Data mínima para filtrar tarefas.
        end_date (datetime): Data máxima para filtrar tarefas.
        creator (str, opcional): Nome do criador para filtrar tarefas.

    Returns:
        list: Lista de dicionários com '_id' (mês, no formato "YYYY-MM") e 'avg_lead_time' (em dias).
    """
    return calculate_monthly_lead_time(MongoDBConnection.get_collection("rr_task_manager", "tasks"), start_date, end_date, creator)