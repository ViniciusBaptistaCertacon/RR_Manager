import requests
import time

HEADERS = {
    "App-Key": "e6b40d7a3927bb80628058a68f48ba58",
    "User-Token": "GKWFVyvw5VdC8rJwuTAR",
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
            "page": page
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
            break

    return all_tasks

def get_all_tasks():
    tasks_open = fetch_paginated_tasks(is_closed=False)
    tasks_closed = fetch_paginated_tasks(is_closed=True)
    return tasks_open + tasks_closed
