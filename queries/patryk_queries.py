from database.connection import MongoDB


def drivers_license_to_expire(db: MongoDB, limit: int = None):
    from datetime import datetime, timedelta

    current_date = datetime.now()

    querry = [
        {
            "$match": {
                "license.expires_on": {"$lte": current_date + timedelta(days=30)},
            }
        },
        {
            "$project": {
                "name": 1,
                "surname": 1,
                "contact.phone": 1,
                "contact.email": 1,
                "license.expires_on": 1,
                "days_left": {"$subtract": ["$license.expires_on", current_date]},
            }
        },
        {
            "$addFields": {
                "days_left": {
                    "$cond": {
                        "if": {"$ne": ["$days_left", 0]},
                        "then": {
                            "$floor": {
                                "$divide": [
                                    "$days_left",
                                    86400000,
                                ]
                            }
                        },
                        "else": 0,
                    }
                }
            }
        },
        {"$sort": {"license.expires_on": 1}},
    ]

    if limit:
        querry.append({"$limit": limit})

    return db.drivers.aggregate(querry)


def print_results(results):
    for result in results:
        print(result)


if __name__ == "__main__":
    db = MongoDB()
    results = drivers_license_to_expire(db, 10)
    print_results(results)
