from data.tasks import get_all_tasks
from infra.mongo_db.settings import MongoDBConnection
from infra.mongo_db.tasks.sync_tasks_repository import sync_tasks

def sync_all_tasks():
    tasks = get_all_tasks()
    tasks_collection = MongoDBConnection.get_collection("rr_task_manager", "tasks")
    reopened_collection = MongoDBConnection.get_collection("rr_task_manager", "reopened_tasks")
    sync_tasks(tasks, tasks_collection, reopened_collection)