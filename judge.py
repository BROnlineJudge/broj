#!/usr/bin/env python
import pika
import sys
import zlib
import time
import tempfile
import subprocess

def usage():
    sys.stderr.write("Usage: TODO")
    sys.exit(1)

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
        code = zlib.decompress(body)
        print(" [x] {0}, {1}".format(method.routing_key, code))
        with tempfile.TemporaryDirectory() as td:
            f = open(td + '/code.cpp', 'w')
            f.write(code.decode())
            f.close()

            print('calling')
            try:
                compilation = subprocess.check_output(args=['g++', f.name, '-o', td + '/prog'], timeout=5)
                print(compilation)
            except subprocess.TimeoutExpired:
                print('TimeoutExpired')
            except subprocess.CalledProcessError:
                print('CalledProcessError')

            try:
                program_output = subprocess.check_output(args=[td + '/prog'], timeout=3)
                print(program_output)
            except subprocess.TimeoutExpired:
                print('TimeoutExpired')
            except subprocess.CalledProcessError:
                print('CalledProcessError')
            except FileNotFoundError:
                print('FileNotFoundError')

            print('called')

            while True:
                pass

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
