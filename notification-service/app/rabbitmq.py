import pika
import json
import os
import logging

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbitmq_port = os.getenv("RABBITMQ_PORT", 5672)
rabbitmq_user = os.getenv("RABBITMQ_USER", "guest")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "guest")

RABBITMQ_URL = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"

logging.basicConfig(level=logging.INFO)

def get_connection():
    """Establish a connection to the RabbitMQ server."""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    return connection

def receive_message(queue_name):
    """Receive a message from the specified queue."""
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    if method_frame:
        message = json.loads(body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        return message
    connection.close()
    return None