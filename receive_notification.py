import pika
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = 'flight_status_updates'
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_notification(contact, message):
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=contact
        )
        print(f"Notification sent to {contact}: {message.sid}")
    except Exception as e:
        print(f"Failed to send notification to {contact}: {e}")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        contact = data.get('contact')
        message = data.get('message')
        if contact and message:
            send_notification(contact, message)
        else:
            print("Invalid message format")
    except Exception as e:
        print(f"Error processing message: {e}")

def receive_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    
    print(f"Waiting for messages in queue '{QUEUE_NAME}'. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    receive_notifications()
