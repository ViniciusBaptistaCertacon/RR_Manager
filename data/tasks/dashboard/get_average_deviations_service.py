from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard import calculate_average_deviations


def get_average_deviations(start_date=None, end_date=None, creator=None):
    """
    Retorna o desvio médio entre as datas planejadas e efetivas para início e término das tarefas,
    aplicando os filtros padrões opcionais.

    Args:
        start_date (datetime, opcional): Data mínima de criação para filtrar tarefas.
        end_date (datetime, opcional): Data máxima de criação para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        dict: Dicionário com 'avg_start_deviation' e 'avg_end_deviation' (em dias).
    """
    return calculate_average_deviations(MongoDBConnection.get_collection("rr_task_manager", "tasks"), start_date, end_date, creator)

