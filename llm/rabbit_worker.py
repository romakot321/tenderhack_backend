import pika
import os

rabbit_host = os.getenv("RABBIT_HOST", "localhost")


class RabbitWorker:
    exchange_in_name = "requests"
    exchange_out_name = "responses"

    def __init__(self, on_message_callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=self.exchange_in_name, exchange_type='fanout')
        self.channel.exchange_declare(exchange=self.exchange_out_name, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange_in_name, queue=self.queue_name)
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=on_message_callback, auto_ack=True
        )

    def run(self):
        channel.start_consuming()

    def answer(self, text):
        return print(text)
        self.channel.basic_publish(exchange=self.exchange_out_name, routing_key='', body=text)
