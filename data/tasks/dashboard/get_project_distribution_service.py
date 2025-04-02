from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard.count_tasks_by_project_repository import count_tasks_by_project


def get_project_distribution(start_date=None, end_date=None, creator=None):
    """
    Retorna a distribuição de tarefas agrupadas por projeto (custom_259), aplicando os filtros opcionais.

    Args:
        start_date (datetime, opcional): Data de início para filtrar tarefas.
        end_date (datetime, opcional): Data de fim para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        list: Lista de dicionários com '_id' (projeto) e 'count'.
    """
    return count_tasks_by_project(MongoDBConnection.get_collection("rr_task_manager", "tasks"), start_date, end_date, creator)