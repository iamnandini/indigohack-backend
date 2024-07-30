import pika
import json

def callback(ch, method, properties, body):
    notification = json.loads(body)
    print(f"Received notification: {notification}")
    # Implement your notification sending logic here (e.g., send email/SMS)

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='flight_status_updates')
    
    channel.basic_consume(queue='flight_status_updates', on_message_callback=callback, auto_ack=True)
    
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
