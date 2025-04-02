from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.dashboard import calculate_tasks_by_professional


def get_tasks_by_professional(period_start, period_end, creator=None):
    """
    Retorna a quantidade de tarefas por profissional (abertas e fechadas) no período informado.

    Args:
        period_start (datetime): Data mínima para o filtro.
        period_end (datetime): Data máxima para o filtro.
        creator (str, opcional): Filtra tarefas que envolvam este profissional.

    Returns:
        list: Lista de documentos com a estrutura:
              {
                  "professional": <id do profissional>,
                  "open_count": <quantidade de tarefas abertas>,
                  "closed_count": <quantidade de tarefas fechadas>
              }
    """
    return calculate_tasks_by_professional(MongoDBConnection.get_collection("rr_task_manager", "tasks"), period_start, period_end, creator)