import json

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from app.config import DefaultSettings
from app.mq import MQEventType, MQManager


settings = DefaultSettings()
rabbitmq_broker = RabbitmqBroker(url=settings.rabbitmq_uri, confirm_delivery=True)
dramatiq.set_broker(rabbitmq_broker)
mqmanager = MQManager()


@dramatiq.actor
def count_words():
    mqmanager.publish_json("events", json.dumps({"user_id": "lala", "event_id": "bobo"}), MQEventType.change)


if __name__ == "__main__":
    count_words.send()
