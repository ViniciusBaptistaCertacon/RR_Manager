import requests
import time
import streamlit as st

#DevOps - ADM - Token - Vinícius
HEADERS = {
    "App-Key": "1a219437eab893dc115509bb85e06d77",
    "User-Token": "9flMUzLxQtxohKGZjU5",
    "Content-Type": "application/json"
}

def fetch_paginated_tasks(is_closed):
    all_tasks = []
    page = 1
    retries = 2
    limit = 100
    base_url = "https://runrun.it/api/v1.0/tasks"

    while True:
        params = {
            "is_closed": str(is_closed).lower(),
            "limit": limit,
            "page": page,
            "sort": "closed_date" if is_closed else "queue_position",
            "sort_dir": "desc" if is_closed else "asc",
            "bypass_status_default": "true"
        }

        attempt = 0
        while attempt <= retries:
            try:
                response = requests.get(base_url, headers=HEADERS, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if not data:
                        return all_tasks
                    all_tasks.extend(data)
                    page += 1
                    break
                else:
                    attempt += 1
                    time.sleep(1)
            except Exception as e:
                attempt += 1
                time.sleep(1)

        if attempt > retries:
            st.warning(f"Falha ao buscar página {page} com is_closed={is_closed} após {retries+1} tentativas.")
            break

    return all_tasks

def get_all_tasks():
    tasks_open = fetch_paginated_tasks(is_closed=False)
    tasks_closed = fetch_paginated_tasks(is_closed=True)
    return tasks_open + tasks_closed
