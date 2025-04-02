from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard.count_tasks_by_status_repository import count_tasks_by_status


def get_task_counts(start_date=None, end_date=None, creator=None):
    """
    Retorna a contagem de tarefas agrupadas por status, aplicando os filtros opcionais.

    Args:
        start_date (datetime, opcional): Data de início para filtrar tarefas.
        end_date (datetime, opcional): Data de fim para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        list: Lista de dicionários com '_id' (status) e 'count'.
    """
    return count_tasks_by_status(MongoDBConnection.get_collection("rr_task_manager", "tasks"), start_date, end_date, creator)