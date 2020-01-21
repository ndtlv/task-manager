import json
import pika


def emit_object_creation(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1'
    ))
    channel = connection.channel()

    channel.queue_declare(queue='objects')

    channel.basic_publish(
        exchange="",
        routing_key="objects",
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )