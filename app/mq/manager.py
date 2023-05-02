import uuid
from datetime import datetime
from typing import Self

import pika

from .type import MQEventType
from app.config import DefaultSettings


settings = DefaultSettings()


class MQManager:
    _instance = None

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_uri))

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def publish_json(self, routing_key: str, body: str, type_: MQEventType) -> None:
        with self.connection.channel() as channel:
            channel.queue_declare(queue=routing_key, durable=True)
            props = pika.BasicProperties(
                content_type="application/json",
                type=type_.value,
                delivery_mode=pika.DeliveryMode.Persistent,
                timestamp=int(datetime.utcnow().timestamp()),
                message_id=str(uuid.uuid4()),
            )
            channel.basic_publish(exchange="", routing_key=routing_key, body=body, properties=props)

    def close(self) -> None:
        self.connection.close()
