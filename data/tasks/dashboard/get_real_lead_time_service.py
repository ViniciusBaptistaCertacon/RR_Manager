from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard import calculate_real_lead_time_by_month


def get_real_lead_time(period_start=None, period_end=None):
    """
    Retorna o lead time real por mês para as tarefas, aplicando filtros de período com base no start_date.

    Filtra apenas as tarefas que possuem start_date e close_date preenchidos.
    Se close_date estiver vazio, a tarefa está em andamento e não é considerada.

    Args:
        period_start (datetime, opcional): Data mínima para o filtro (aplicada em start_date).
        period_end (datetime, opcional): Data máxima para o filtro (aplicada em start_date).

    Returns:
        list: Lista de dicionários com os dados do lead time real por mês.
    """
    collection = MongoDBConnection.get_collection("rr_task_manager", "tasks")
    return calculate_real_lead_time_by_month(collection, start_date=period_start, end_date=period_end)
