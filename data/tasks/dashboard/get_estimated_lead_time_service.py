from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard import calculate_estimated_lead_time_by_month




def get_estimated_lead_time(period_start=None, period_end=None):
    """
    Retorna o lead time estimado por mês para as tarefas, aplicando filtros de período com base no custom_fields.custom_270.

    Filtra apenas as tarefas que possuem custom_fields.custom_270 e custom_fields.custom_272 preenchidos.
    Se custom_fields.custom_272 estiver vazio, a tarefa está em andamento e não é considerada.

    Args:
        period_start (datetime, opcional): Data mínima para o filtro (aplicada em custom_fields.custom_270).
        period_end (datetime, opcional): Data máxima para o filtro (aplicada em custom_fields.custom_270).

    Returns:
        list: Lista de dicionários com os dados do lead time estimado por mês.
    """
    collection = MongoDBConnection.get_collection("rr_task_manager", "tasks")
    return calculate_estimated_lead_time_by_month(collection, start_date=period_start, end_date=period_end)
