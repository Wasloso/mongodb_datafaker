from pymongo import MongoClient
from datetime import datetime
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

rides= db["rides"]
most_rode_lines = rides.aggregate([
    {
        "$group": {
            "_id": "$line_id",  
            "total_rides": {"$sum": 1}  
        }
    },
    {
        "$sort": {"total_rides": -1} 
    },
    {
        "$project": {
            "_id": 0,
            "line_id": "$_id",
            "total_rides": 1
        }
    },
    {
        "$limit": 10
    }
])

print("Drivers with expired licenses:")
for driver in expired_drivers:
    print(driver)

# print("\nMonthly income:")
# for entry in monthly_income:
#     print(entry)

print("\nVehicles with issues:")
for vehicle in vehicles_with_issues:
    print(vehicle)

print("\nPassengers with overdue fines:")
for passenger in overdue_fines:
    print(passenger)

print("\nTicket ranking:")
for ticket in ticket_ranking:
    print(ticket)

print("\nMost rode lines:")
for line in most_rode_lines:
    print(line)