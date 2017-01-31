#!/usr/bin/env python
import pika
import zlib
from verdict import Verdict

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='courier')#, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    rc = zlib.decompress(body)
    print(f' [x] Received {rc}')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='courier')

channel.start_consuming()
