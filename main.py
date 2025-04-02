from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException

from data.tasks import sync_all_tasks
from data.tasks.dashboard import (
    get_task_counts, get_real_lead_time, get_estimated_lead_time
)

app = FastAPI(
    title="Task Manager API",
    description="API para gerenciamento de tarefas com operações de sincronização e dashboards.",
    version="1.0.0"
)

@app.post("/tasks/sync", tags=["Tasks"])
def sync_tasks():
    """
    Sincroniza todas as tarefas.

    Endpoint que dispara a sincronização das tarefas, utilizando os repositórios e conexões definidos.
    """
    try:
        sync_all_tasks()
        return {"message": "Tarefas sincronizadas com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/task-counts", tags=["Dashboard"])
def task_counts(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        creator: Optional[str] = None
):
    """
    Retorna a contagem de tarefas agrupadas por status, aplicando filtros opcionais.

    - **start_date**: Data de início para filtrar tarefas (opcional).
    - **end_date**: Data de fim para filtrar tarefas (opcional).
    - **creator**: Nome do criador da tarefa (opcional).
    """
    try:
        counts = get_task_counts(start_date, end_date, creator)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/real-lead-time", tags=["Dashboard"])
def real_lead_time(
        period_start: datetime,
        period_end: datetime
):
    """
    Retorna o lead time real por mês para o período informado.

    - **period_start**: Data mínima para o filtro (aplicada em start_date).
    - **period_end**: Data máxima para o filtro (aplicada em start_date).
    """
    try:
        result = get_real_lead_time(period_start, period_end)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/estimated-lead-time", tags=["Dashboard"])
def estimated_lead_time(
        period_start: datetime,
        period_end: datetime
):
    """
    Retorna o lead time estimado por mês para o período informado.

    - **period_start**: Data mínima para o filtro (aplicada em custom_fields.custom_270).
    - **period_end**: Data máxima para o filtro (aplicada em custom_fields.custom_270).
    """
    try:
        result = get_estimated_lead_time(period_start, period_end)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))