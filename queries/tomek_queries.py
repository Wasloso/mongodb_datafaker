from pymongo import MongoClient
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.connection import MongoDB

mongo= MongoDB()
client = MongoClient(mongo.uri)
db = client[str(mongo.db_name)]

# Best-selling tickets in the last 6 months
tickets_collection = db["tickets"]
six_months_ago = datetime.utcnow() - timedelta(days=180)
best_selling_tickets = tickets_collection.aggregate([
    {"$match": {"purchase.date": {"$gte": six_months_ago}}},
    {"$group": {"_id": "$ticket_type_id", "totalPurchases": {"$sum": 1}}},
    {"$sort": {"totalPurchases": -1}},
    {"$lookup": {
        "from": "ticket_types",
        "localField": "_id",
        "foreignField": "_id",
        "as": "ticket_type_info"
        }
    },
    {"$unwind": "$ticket_type_info"},
    {"$project": {
        "ticket_type_info.name": 1,
        "ticket_type_info.price": 1,
        "ticket_type_info.type": 1,
        "totalPurchases": 1,
        "_id": 0
    }}
])

# Number of inspections per line in 2024
inspections_collection = db["inspections"]
inspections_per_line = inspections_collection.aggregate([
    {"$match": {
        "date": {
            "$gte": datetime(2024, 1, 1),
            "$lt": datetime(2025, 1, 1)
            }
        }
    },
    {"$lookup": {
        "from": "rides",
        "localField": "ride_id",
        "foreignField": "_id",
        "as": "ride_info"
        }
    },
    {"$unwind": "$ride_info"},
    {"$group": {
        "_id": {
            "line_id": "$ride_info.line_id"
            }, 
        "totalInspections": {
            "$sum": 1
            }
        }
    },
    {"$sort": {"totalInspections": -1}},
    {"$lookup": {
        "from": "lines",
        "localField": "_id.line_id",
        "foreignField": "_id",
        "as": "line_info"
        }
    },
    {"$unwind": "$line_info"},
    {"$project": {
        "line_number": "$line_info.number",
        "totalInspections": 1,
        "_id": 0
        }
    }
])

# Total repair costs over the years
vehicles_collection = db["vehicles"]
vehicle_repairs = vehicles_collection.aggregate([
    {"$unwind": "$technical_issues"},
    {"$match": {
        "technical_issues.status": "resolved",
        "technical_issues.resolve_date": {"$ne": None},
        "technical_issues.repair_cost": {"$ne": None}
    }},
    {"$project": {
        "year": {
            "$year": "$technical_issues.resolve_date"
            },
        "repair_cost": "$technical_issues.repair_cost"
        }
    },
    {"$group": {
        "_id": "$year",
        "totalRepairCost": {
            "$sum": "$repair_cost"
            }
        }
    },
    {"$sort": {"_id": -1}}
])


def print_results(title, cursor):
    print(f"\n{title}:")
    for doc in cursor:
        print(doc)

print_results("Best-selling tickets in the last 6 months", best_selling_tickets)
print_results("Number of inspections per line in 2024", inspections_per_line)
print_results("Total repair costs over the years", vehicle_repairs)