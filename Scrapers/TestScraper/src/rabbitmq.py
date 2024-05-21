import pika
import json
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "guest")
scraper_name = os.getenv("SCRAPER_NAME", "DefaultScraper")

RABBITMQ_URL = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"

def get_connection():
    """Establish a connection to the RabbitMQ server."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    return connection

def send_message(queue_name, data_type, message):
    """Send a message to a specific queue in RabbitMQ."""
    connection = get_connection()
    try:
        channel = connection.channel()
        full_queue_name = f"{scraper_name}.{queue_name}.{data_type}"
        channel.queue_declare(queue=full_queue_name, durable=True)
        channel.basic_publish(
            exchange="", 
            routing_key=full_queue_name, 
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
    finally:
        connection.close()
