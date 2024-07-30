from apscheduler.schedulers.background import BackgroundScheduler
from models import flights_collection, passengers_collection, scheduled_flights_collection
import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = 'flight_status_updates'

def get_rabbit_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

def check_flight_updates():
    # Get live flight data
    live_flights = flights_collection.find({})
    
    for live_flight in live_flights:
        flight_id = live_flight['flight_id']
        live_status = live_flight['remark']
        
        # Get corresponding scheduled flight data
        scheduled_flight = scheduled_flights_collection.find_one({'flight_id': flight_id})
        
        if scheduled_flight and live_status != scheduled_flight['remark']:
            # Find passengers subscribed to the flight
            passengers = list(passengers_collection.find({'flight_id': flight_id}))

            # Send notifications to each passenger
            connection = get_rabbit_connection()
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)

            for passenger in passengers:
                notification = {
                    'passenger_id': str(passenger['_id']),
                    'contact': passenger['mobile'],
                    'message': f"Flight {flight_id} status update: {live_status}"
                }
                channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=json.dumps(notification),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    )
                )

            connection.close()

            # Update the scheduled_flight to reflect the new status
            scheduled_flights_collection.update_one({'flight_id': flight_id}, {'$set': {'remark': live_status}})

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_flight_updates, 'interval', minutes=1)  # Check every minute
    scheduler.start()

if __name__ == '__main__':
    start_scheduler()
