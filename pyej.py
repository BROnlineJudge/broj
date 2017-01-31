import pika

class Judge():
    def __init__(self, hostname):
        print('judge init')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hostname))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='xch_topic_pyej',
                                 exchange_type='topic')

    def __del__(self):
        print('judge del')
        self.connection.close()

    def send(self, rk, msg):
        self.channel.basic_publish(exchange='xch_topic_pyej',
                      routing_key=rk,
                      body=msg)
