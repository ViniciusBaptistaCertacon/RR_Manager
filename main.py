from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException

from data.tasks import sync_all_tasks
from data.tasks.dashboard import (
    get_task_counts, get_monthly_lead_time, get_project_distribution, get_average_deviations, get_tasks_by_professional
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

@app.get("/dashboard/project-distribution", tags=["Dashboard"])
def project_distribution(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        creator: Optional[str] = None
):
    """
    Retorna a distribuição de tarefas agrupadas por projeto, aplicando filtros opcionais.

    - **start_date**: Data de início para filtrar tarefas (opcional).
    - **end_date**: Data de fim para filtrar tarefas (opcional).
    - **creator**: Nome do criador da tarefa (opcional).
    """
    try:
        distribution = get_project_distribution(start_date, end_date, creator)
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/average-deviations", tags=["Dashboard"])
def average_deviations(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        creator: Optional[str] = None
):
    """
    Retorna o desvio médio entre as datas planejadas e efetivas para início e término das tarefas,
    aplicando filtros opcionais.

    - **start_date**: Data mínima de criação para filtrar tarefas (opcional).
    - **end_date**: Data máxima de criação para filtrar tarefas (opcional).
    - **creator**: Nome do criador da tarefa (opcional).
    """
    try:
        deviations = get_average_deviations(start_date, end_date, creator)
        return deviations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/lead", tags=["Dashboard"])
def monthly_lead_time(
        start_date: datetime,
        end_date: datetime,
        creator: Optional[str] = None
):
    """
    Retorna, por mês, o lead time médio (em dias) calculado a partir de gantt_bar_start_date até close_date,
    para as tarefas finalizadas dentro do período informado.

    - **start_date**: Data mínima para filtrar tarefas (aplicada em gantt_bar_start_date).
    - **end_date**: Data máxima para filtrar tarefas (aplicada em gantt_bar_start_date).
    - **creator**: Nome do criador da tarefa (opcional).
    """
    try:
        lead_time = get_monthly_lead_time(start_date, end_date, creator)
        return lead_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/professional-tasks", tags=["Dashboard"])
def professional_tasks(
        period_start: datetime,
        period_end: datetime,
        creator: Optional[str] = None
):
    """
    Retorna, para o período informado, a quantidade de tarefas por profissional,
    separando itens em aberto e fechados.

    - **period_start**: Data mínima para o filtro (aplicada em 'created_at' para itens abertos
      e em 'close_date' para itens fechados).
    - **period_end**: Data máxima para o filtro.
    - **creator**: (Opcional) Filtra tarefas que envolvam este profissional.
    """
    try:
        result = get_tasks_by_professional(period_start, period_end, creator)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))