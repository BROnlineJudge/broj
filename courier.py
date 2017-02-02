#!/usr/bin/env python
import pika
import zlib
import json
from ej.verdict import Verdict
from ej import consts

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=consts.courier_queue)#, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    msg_from_judge = json.loads(zlib.decompress(body).decode())
    print(f' [x] Received {msg_from_judge}')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=consts.courier_queue)

channel.start_consuming()
