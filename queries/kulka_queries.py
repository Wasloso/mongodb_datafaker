from pymongo import MongoClient
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from models.ticket import purchase
from database.connection import MongoDB

mongo= MongoDB()
client = MongoClient(mongo.uri)
db = client[str(mongo.db_name)] 
drivers_collection = db["drivers"]

expired_drivers = drivers_collection.aggregate([
    {
        "$match": {
            "license.expires_on": {"$lt": datetime.utcnow()}
        }
    },
    {
        "$sort": {
            "license.expires_on": 1  
        }
    },
    {
        "$project": {
            "_id": 0,
            "name": "$user.name",
            "surname": "$user.surname",
            "id_driver": 1,
            "issued_on": "$license.issued_on",
            "expires_on": "$license.expires_on"
        }
    }
])

purchases_collection = db["users"]  
monthly_income = purchases_collection.aggregate([
    {
        "$group": {
            "_id": {"$month": "$date"},  
            "total_income_per_month": {"$sum": "$amount"}  
        }
    },
    {
        "$sort": {
            "total_income_per_month": 1  
        }
    },
    {
        "$project": {
            "_id": 0,
            "month": "$_id",
            "total_income_per_month": 1
        }
    }
])
vehicles_collection = db["vehicles"]

vehicles_with_issues = vehicles_collection.aggregate([
    {
        
        "$match": {
            "technical_issues": {"$gt": []}
        },
    },
    {
        "$project": {
            "_id": 0,
            "id_vehicle": 1,
            "vehicle_number": 1,
            "production_date": 1,
            "last_technical_inspection": 1,
            "status": 1,
            "count_issues": {"$size": {"$ifNull": ["$technical_issues", []]}}  
        }
    },
    {
        "$sort": {
            "count_issues": -1  
        }
    }
])

passengers_collection = db["passengers"]

now = datetime.utcnow()

overdue_fines = passengers_collection.aggregate([
    {
        "$unwind": "$unpaid_fines"  
    },
    {
        "$match": {
            "unpaid_fines.deadline": {"$lt": now}  
        }
    },
    {
        "$sort": {
            "unpaid_fines.deadline": 1  
        }
    },
    {
        "$project": {
            "_id": 0,
            "name": 1,
            "surname": 1,
            "login": 1,
            "contact": 1, 
            "deadline": "$unpaid_fines.deadline",
            "amount": "$unpaid_fines.amount"
        }
    },
    {
        "$limit": 5
    }
])
ticket_ranking = passengers_collection.aggregate([
    {
        "$unwind": "$active_tickets"  
    },
    {
        "$group": {
            "_id": "$active_tickets.name",  
            "total_sold": {"$sum": 1}  
        }
    },
    {
        "$sort": {"total_sold": -1} 
    },
    {
        "$project": {
            "_id": 0,
            "ticket_name": "$_id",
            "total_sold": 1
        }
    }
])

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

print_results("Drivers with expired licenses", expired_drivers)
print_results("Monthly income", monthly_income)
print_results("Vehicles with issues", vehicles_with_issues)
print_results("Passengers with overdue fines", overdue_fines)
print_results("Ticket ranking", ticket_ranking)
print_results("Best-selling tickets in the last 6 months", best_selling_tickets)
print_results("Number of inspections per line in 2024", inspections_per_line)
print_results("Total repair costs over the years", vehicle_repairs)