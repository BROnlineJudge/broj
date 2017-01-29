#!/usr/bin/env python
import pika
import sys
import zlib
import time

g_valid_languages = ['c++', 'c', 'python', 'java', 'ruby']

def usage():
    sys.stderr.write("Usage: ")
    sys.stderr.write("{0} {1}\n".format(sys.argv[0], g_valid_languages))
    sys.exit(1)

def valid_language(language):
    return language in g_valid_languages

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='xch_topic_pyej',
                             exchange_type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    languages = sys.argv[1:]
    if not languages:
        usage()

    for language in languages:
        channel.queue_bind(exchange='xch_topic_pyej',
                           queue=queue_name,
                           routing_key=language)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] {0}, {1}".format(method.routing_key, zlib.decompress(body)))

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
