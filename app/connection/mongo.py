import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')

# Print to verify they are correctly set (Remove or comment out in production)
print(f"MONGO_USER: {mongo_user}, MONGO_PASSWORD: {mongo_password}")

# Construct the connection string
connection_string = f"mongodb+srv://{mongo_user}:{mongo_password}@ruleengine.yosgt6d.mongodb.net/?retryWrites=true&w=majority&appName=RuleEngine"

try:
    # Create a MongoClient
    client = MongoClient(connection_string)
    # Access the database
    db = client['RuleEngine']
    # Access the collection
    rules_collection = db.test
    
    # Test the connection
    print("Connected to MongoDB!")
    print("Collection names:", db.list_collection_names())
except Exception as e:
    print("Could not connect to MongoDB:", e)
