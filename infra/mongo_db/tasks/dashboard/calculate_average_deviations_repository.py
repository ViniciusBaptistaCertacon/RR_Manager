def calculate_average_deviations(tasks_collection, start_date=None, end_date=None, creator=None):
    """
    Calcula o desvio médio entre as datas planejadas e as efetivas para o início e término das tarefas.
    O desvio é calculado como:
      - Início: start_date - gantt_bar_start_date
      - Término: close_date - gantt_bar_end_date (apenas para tarefas finalizadas)
    Os resultados são convertidos para dias.

    Permite filtrar as tarefas com base na data de criação (created_at) e no nome do criador (user_name).

    Args:
        tasks_collection: Coleção de tarefas no MongoDB.
        start_date (datetime, opcional): Data mínima de criação para filtrar tarefas.
        end_date (datetime, opcional): Data máxima de criação para filtrar tarefas.
        creator (str, opcional): Nome do criador da tarefa para filtrar.

    Returns:
        dict: Dicionário com 'avg_start_deviation' e 'avg_end_deviation' (em dias),
              ou None se não houver dados para o cálculo.
    """
    query = {}
    if start_date or end_date:
        query["created_at"] = {}
        if start_date:
            query["created_at"]["$gte"] = start_date
        if end_date:
            query["created_at"]["$lte"] = end_date
    if creator:
        query["user_name"] = creator

    pipeline = []
    if query:
        pipeline.append({"$match": query})

    pipeline.append({
        "$facet": {
            "start_deviation": [
                {"$match": {
                    "start_date": {"$exists": True, "$ne": None},
                    "gantt_bar_start_date": {"$exists": True, "$ne": None}
                }},
                {"$project": {
                    "start_deviation": {
                        "$divide": [
                            {"$subtract": [
                                {"$toDate": "$start_date"},
                                {"$toDate": "$gantt_bar_start_date"}
                            ]},
                            86400000
                        ]
                    }
                }},
                {"$group": {
                    "_id": None,
                    "avg_start_deviation": {"$avg": "$start_deviation"}
                }}
            ],
            "end_deviation": [
                {"$match": {
                    "close_date": {"$exists": True, "$ne": None},
                    "gantt_bar_end_date": {"$exists": True, "$ne": None}
                }},
                {"$project": {
                    "end_deviation": {
                        "$divide": [
                            {"$subtract": [
                                {"$toDate": "$close_date"},
                                {"$toDate": "$gantt_bar_end_date"}
                            ]},
                            86400000
                        ]
                    }
                }},
                {"$group": {
                    "_id": None,
                    "avg_end_deviation": {"$avg": "$end_deviation"}
                }}
            ]
        }
    })

    pipeline.append({
        "$project": {
            "avg_start_deviation": {"$arrayElemAt": ["$start_deviation.avg_start_deviation", 0]},
            "avg_end_deviation": {"$arrayElemAt": ["$end_deviation.avg_end_deviation", 0]}
        }
    })

    result = list(tasks_collection.aggregate(pipeline))
    return result[0] if result else None