import pika
import os

rabbit_host = os.getenv("RABBIT_HOST", "localhost")


class RabbitWorker:
    exchange_in_name = "requests"
    exchange_out_name = "responses"

    def __init__(self, on_message_callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange_in_name, exchange_type='direct')
        self.channel.exchange_declare(exchange=self.exchange_out_name, exchange_type='direct')

        result = self.channel.queue_declare(queue='llm', durable=True, exclusive=False, auto_delete=False)
        self.queue_name = result.method.queue
        print("Declared queue with name", self.queue_name)
        self.channel.queue_bind(exchange=self.exchange_in_name, queue=self.queue_name, routing_key='in')
        print("Starting consuming...")
        self.channel.basic_consume(
            queue=self.queue_name, exchange=self.exchange_in_name, on_message_callback=on_message_callback, auto_ack=True
        )

    def run(self):
        self.channel.start_consuming()

    def answer(self, text):
        self.channel.basic_publish(exchange=self.exchange_out_name, routing_key='out', body=text)
        print("Sended", text)
