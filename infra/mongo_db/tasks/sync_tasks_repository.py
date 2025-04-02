import time
from pymongo import UpdateOne, InsertOne
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sync_tasks(json_tasks, tasks_collection, reopened_collection):
    """
    Sincroniza a lista de tarefas (json_tasks) com a coleção tasks_collection do MongoDB.
    Para cada tarefa, se ela já existir, atualiza seus campos; se não, insere como nova.
    Se a tarefa já existia com status "*FINALIZADAS" e o novo status for diferente,
    registra a reabertura na coleção reopened_collection com a data da reabertura e o id da tarefa.

    Args:
        json_tasks (list): Lista de dicionários representando as tarefas.
        tasks_collection: Objeto da coleção de tarefas no MongoDB.
        reopened_collection: Objeto da coleção para registrar tarefas reabertas.

    Returns:
        dict: Resultado da operação bulk_write na coleção de tarefas.
    """
    if not isinstance(json_tasks, list):
        raise ValueError("json_tasks deve ser uma lista de dicionários.")

    tasks_by_id = {task['id']: task for task in json_tasks if 'id' in task}
    json_ids = list(tasks_by_id.keys())

    db_tasks_cursor = tasks_collection.find({"id": {"$in": json_ids}})
    db_tasks_by_id = {doc["id"]: doc for doc in db_tasks_cursor}

    bulk_ops = []
    reopened_docs = []

    for task_id, task in tasks_by_id.items():
        novo_status = task.get("board_stage_name")
        update_fields = {
            "title": task.get("title"),
            "board_stage_name": novo_status,
            "is_closed": task.get("is_closed"),
            "status": novo_status,
            "completion_date": task.get("close_date"),
            "custom_fields": task.get("custom_fields"),
            "assignments": task.get("assignments")
        }

        if task_id in db_tasks_by_id:
            existing_status = db_tasks_by_id[task_id].get("status")
            if existing_status == "*FINALIZADAS" and novo_status != "*FINALIZADAS":
                reopened_docs.append({
                    "task_id": task_id,
                    "reopened_at": datetime.now()
                })
            bulk_ops.append(UpdateOne({"id": task_id}, {"$set": update_fields}))
        else:
            new_doc = task.copy()
            new_doc["status"] = novo_status
            new_doc["completion_date"] = task.get("close_date") if task.get("is_closed") else None
            bulk_ops.append(InsertOne(new_doc))

    result = None
    if bulk_ops:
        result = tasks_collection.bulk_write(bulk_ops)
        logger.info("Bulk operation completed. Matched: %d, Modified: %d, Inserted: %d",
                    result.matched_count, result.modified_count, result.inserted_count)

    if reopened_docs:
        reopened_collection.insert_many(reopened_docs)
        logger.info("Registradas %d reaberturas", len(reopened_docs))

    return result.bulk_api_result if result else None
