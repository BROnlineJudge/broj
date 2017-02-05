import pika
import json
import zlib
from ej import consts

def compress(message):
    return zlib.compress(json.dumps(message).encode())

def decompress(message):
    return json.loads(zlib.decompress(message).decode())

class JudgeConnectionError(Exception):
    pass

class JudgeConnection():
    def __init__(self, host, language):
        self.host = host
        self.language = language
        self.connection = None
        self.channel = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()
        self.connection.close()

    def connect(self, attempts=3):
        # Prevent declaring an invalid durable queue.
        if self.language not in consts.languages:
            raise JudgeConnectionError

        try:
            params = pika.ConnectionParameters(host=self.host,
                                               connection_attempts=attempts)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.confirm_delivery()
            self.channel.exchange_declare(exchange=consts.judge_exchange,
                                          exchange_type=consts.judge_exchange_type)
            self.channel.queue_declare(queue=self.language, durable=True)
            self.channel.queue_bind(exchange=consts.judge_exchange,
                                    queue=self.language,
                                    routing_key=self.language)
        except Exception as e:
            raise JudgeConnectionError

    def send(self, message):
        try:
            properties = pika.BasicProperties(
                delivery_mode = consts.rmq_persistent_message)
            self.channel.publish(exchange=consts.judge_exchange,
                            routing_key=self.language, body=compress(message),
                            mandatory=True, properties=properties)
        except Exception as e:
            raise JudgeConnectionError

    def consume(self, callback, prefetch_count=1):
        try:
            self.channel.basic_qos(prefetch_count=prefetch_count)
            self.channel.basic_consume(callback, queue=self.language)
            self.channel.start_consuming()
        except Exception as e:
            raise JudgeConnectionError


class CourierConnectionError(Exception):
    pass

class CourierConnection():
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()
        self.connection.close()

    def connect(self, attempts=3):
        try:
            params = pika.ConnectionParameters(host=self.host,
                                               connection_attempts=attempts)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.confirm_delivery()
            self.channel.exchange_declare(exchange=consts.courier_exchange,
                                          exchange_type=consts.courier_exchange_type)
            self.channel.queue_declare(queue=consts.courier_queue, durable=True)
            self.channel.queue_bind(exchange=consts.courier_exchange,
                                    queue=consts.courier_queue,
                                    routing_key=consts.courier_rk)
        except Exception as e:
            raise CourierConnectionError

    def send(self, message):
        try:
            properties = pika.BasicProperties(
                delivery_mode = consts.rmq_persistent_message)
            self.channel.publish(exchange=consts.courier_exchange,
                            routing_key=consts.courier_rk, body=compress(message),
                            mandatory=True, properties=properties)
        except Exception as e:
            raise CourierConnectionError

    def consume(self, callback, prefetch_count=1):
        try:
            self.channel.basic_qos(prefetch_count=prefetch_count)
            self.channel.basic_consume(callback, queue=consts.courier_queue)
            self.channel.start_consuming()
        except Exception as e:
            raise CourierConnectionError
