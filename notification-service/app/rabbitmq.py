import pika
import json
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "guest")

RABBITMQ_URL = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"

def get_connection():
    """Establish a connection to the RabbitMQ server."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    return connection

# TODO - Implement the Subscriber class, which will be used to subscribe to RabbitMQ queues
# IDEAS:
# - Able to connect to a specific Exchange
# - Able to subscribe to a specific queue
# - Able to define routing keys
# returns a channel object