from flask import Flask, jsonify, request
import pika
import json
from flask_cors import CORS
from models import flights_collection, passengers_collection, scheduled_flights_collection
from monitor import start_scheduler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'flight_status_updates'

# Setup RabbitMQ connection
def get_rabbit_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

@app.route('/api/flight-status', methods=['GET'])
def get_flight_status():
    live_flights = list(flights_collection.find({}))
    for flight in live_flights:
        flight['_id'] = str(flight['_id'])  # Convert ObjectId to string

    return jsonify(live_flights)

@app.route('/api/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    flight_id = data.get('flight_id')
    status_update = data.get('status_update')

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
            'message': f"Flight {flight_id} status update: {status_update}"
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
    return jsonify({"message": "Notifications sent"}), 200

if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True)
