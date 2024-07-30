from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)

db = client['flight_notifications']
flights_collection = db['flight_live']
passengers_collection = db['passengers']
scheduled_flights_collection = db['scheduled_flights']
