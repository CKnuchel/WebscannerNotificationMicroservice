import pika
import json
import os

rabiitmq_host = "rabbitmq"
rabbitmq_port = os.getenv("RABBITMQ_AMQP_PORT", 5672)
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
scraper_name = os.getenv("TEST_SCRAPER_NAME", "TestScraper")

RABBITMQ_URL = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabiitmq_host}:{rabbitmq_port}"

def get_connection():
    """
    This function is used to establish a connection to the RabbitMQ server.
    - Returns: The connection object
    """
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    return connection

def send_message(queue_name, data_type, message):
    """
    This function is used to send a message to a specific queue in the RabbitMQ server.
    - queue_name: The name of the queue to send the message to
    - message: The message to send
    """
    connection = get_connection()
    channel = connection.channel()
    queue_name = f"{scraper_name}.{queue_name}.{data_type}"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange="", 
                          routing_key=queue_name, 
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()
