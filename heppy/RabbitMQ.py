#!/usr/bin/env python

import pika
import uuid

class RPCServer:
    def __init__(self, config):
        self.config = config
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['RabbitMQ']['host'],
        ))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config['queue'])
        self.channel.basic_qos(prefetch_count=1)

    def consume(self, response):
        self.response = response
        self.channel.basic_consume(self.on_request, self.config['queue'])

        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        reply = self.response(body)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id = props.correlation_id,
            ),
            body=str(reply),
        )
        ch.basic_ack(delivery_tag = method.delivery_tag)

class RPCClient:
    def __init__(self, config):
        self.config = config
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['RabbitMQ']['host'],
        ))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.reply_queue = result.method.queue

        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.reply_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.reply = body

    def request(self, query):
        self.reply = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
            routing_key=self.config['queue'],
            properties=pika.BasicProperties(
                reply_to = self.reply_queue,
                correlation_id = self.corr_id,
            ),
            body=str(query)
        )
        while self.reply is None:
            self.connection.process_data_events()
        return self.reply

