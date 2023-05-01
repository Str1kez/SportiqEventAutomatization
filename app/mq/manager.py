from datetime import datetime
from typing import Self

import pika

from .type import MQEventType
from app.config import DefaultSettings


class MQManager:
    def __init__(self) -> None:
        settings = DefaultSettings()
        self.connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_uri))

    def __new__(cls) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super(MQManager, cls).__new__(cls)
        return cls.instance  # noqa

    def publish_json(self, routing_key: str, body: str, type_: MQEventType) -> None:
        channel = self.connection.channel()
        channel.queue_declare(queue=routing_key, durable=True)
        props = pika.BasicProperties(
            content_type="application/json",
            type=type_.value,
            delivery_mode=pika.DeliveryMode.Persistent,
            timestamp=int(datetime.utcnow().timestamp()),
        )
        channel.basic_publish(exchange="", routing_key=routing_key, body=body, properties=props)

    def __del__(self) -> None:
        self.connection.close()
