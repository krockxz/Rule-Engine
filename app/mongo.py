import os
from pymongo import MongoClient

mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
connection_string = f"mongodb+srv://{mongo_user}:{mongo_password}@ruleengine.yosgt6d.mongodb.net/?retryWrites=true&w=majority&appName=RuleEngine"

client = MongoClient(connection_string)
db = client['RuleEngine']
rules_collection = db.test


