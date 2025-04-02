import logging

logger = logging.getLogger(__name__)

def calculate_tasks_by_professional(tasks_collection, period_start, period_end, professional_id=None):
    """
    Calcula a quantidade de tarefas abertas e concluídas por profissional em um período.

    Regras:
    - Tarefa concluída: is_closed = True e close_date dentro do período.
    - Tarefa em aberto: is_closed = False ou close_date ausente, e criada antes ou durante o período.
    - Se professional_id for informado, filtra tasks em que ele seja responsável direto ou designado.

    Args:
        tasks_collection: MongoDB collection.
        period_start (datetime): Data inicial do filtro.
        period_end (datetime): Data final do filtro.
        professional_id (str, optional): ID do profissional (responsável ou designado).

    Returns:
        list: [
            {
                "professional": "nome_id",
                "open_count": 5,
                "closed_count": 12
            },
            ...
        ]
    """
    pipeline = [
        {"$addFields": {
            "closed_at_dt": {"$toDate": "$close_date"},
            "created_at_dt": {"$toDate": "$created_at"}
        }},
        {"$match": {
            "$or": [
                {
                    "$and": [
                        {"is_closed": True},
                        {"closed_at_dt": {"$gte": period_start, "$lte": period_end}}
                    ]
                },
                {
                    "$and": [
                        {"$or": [{"is_closed": False}, {"close_date": None}]},
                        {"created_at_dt": {"$lte": period_end}},
                        {"$or": [
                            {"close_date": None},
                            {"closed_at_dt": {"$gt": period_end}}
                        ]}
                    ]
                }
            ]
        }},
    ]

    if professional_id:
        pipeline.append({
            "$match": {
                "$expr": {
                    "$or": [
                        {"$eq": ["$responsible_id", professional_id]},
                        {"$in": [
                            professional_id,
                            {"$ifNull": [
                                {"$map": {
                                    "input": "$assignments",
                                    "as": "a",
                                    "in": "$$a.assignee_id"
                                }},
                                []
                            ]}
                        ]}
                    ]
                }
            }
        })

    pipeline += [
        {"$set": {
            "professionals": {
                "$setUnion": [
                    {"$cond": [{"$ne": ["$responsible_id", None]}, ["$responsible_id"], []]},
                    {"$ifNull": [
                        {"$map": {
                            "input": "$assignments",
                            "as": "a",
                            "in": "$$a.assignee_id"
                        }},
                        []
                    ]}
                ]
            }
        }},
        {"$unwind": "$professionals"},
        {"$set": {
            "status": {"$cond": [{"$eq": ["$is_closed", True]}, "closed", "open"]}
        }},
        {"$group": {
            "_id": {"professional": "$professionals", "status": "$status"},
            "count": {"$sum": 1}
        }},
        {"$group": {
            "_id": "$_id.professional",
            "counts": {"$push": {"status": "$_id.status", "count": "$count"}}
        }},
        {"$project": {
            "professional": "$_id",
            "open_count": {
                "$ifNull": [
                    {"$first": {
                        "$map": {
                            "input": {
                                "$filter": {
                                    "input": "$counts",
                                    "as": "c",
                                    "cond": {"$eq": ["$$c.status", "open"]}
                                }
                            },
                            "as": "f",
                            "in": "$$f.count"
                        }
                    }},
                    0
                ]
            },
            "closed_count": {
                "$ifNull": [
                    {"$first": {
                        "$map": {
                            "input": {
                                "$filter": {
                                    "input": "$counts",
                                    "as": "c",
                                    "cond": {"$eq": ["$$c.status", "closed"]}
                                }
                            },
                            "as": "f",
                            "in": "$$f.count"
                        }
                    }},
                    0
                ]
            }
        }}
    ]

    logger.info("Calculando tarefas por profissional para o período de %s a %s", period_start, period_end)
    return list(tasks_collection.aggregate(pipeline))
