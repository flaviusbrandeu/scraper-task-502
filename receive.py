import json

import os
import pika
import sys
from scrapy.utils.project import get_project_settings


class RabbitMQReader(object):
    def __init__(self, host, port, user, password, virtual_host, exchange, routing_key, queue):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.virtual_host = virtual_host
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                               self.port,
                                               self.virtual_host,
                                               credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue = queue
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type="direct",
                                      durable=True)
        self.channel.queue_declare(queue=queue,
                                   durable=True)
        self.channel.queue_bind(exchange=exchange,
                                routing_key=routing_key,
                                queue=queue)

    def close_spider(self, spider):
        self.channel.close()
        self.connection.close()

    def print_urls(self):
        def callback(ch, method, properties, body):
            my_json = body.decode('utf8')
            data = json.loads(my_json)
            print(data['url'])

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    @staticmethod
    def find_all_substrings(string, sub):
        import re
        starts = [match.start() for match in re.finditer(re.escape(sub), string)]
        return starts

    def check_keywords(self):
        words = [
            "mentor",
            "Blog",
            "Developer to Manager",
        ]

        def callback(ch, method, properties, body):
            json_content = body.decode('utf8')
            data = json.loads(json_content)
            webpage_text = data['text']
            for word in words:
                substrings = self.find_all_substrings(webpage_text, word)
                for _ in substrings:
                    print(f"[{word}] -> {data['url']}")

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


if __name__ == '__main__':
    try:
        settings = get_project_settings()
        rabbitmq_reader = RabbitMQReader(
            host=settings.get("RABBITMQ_HOST"),
            port=settings.get("RABBITMQ_PORT"),
            user=settings.get("RABBITMQ_USER"),
            password=settings.get("RABBITMQ_PASSWORD"),
            virtual_host=settings.get("RABBITMQ_VIRTUAL_HOST"),
            exchange=settings.get("RABBITMQ_EXCHANGE"),
            routing_key=settings.get("RABBITMQ_ROUTING_KEY"),
            queue=settings.get("RABBITMQ_QUEUE")
        )
        rabbitmq_reader.check_keywords()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
