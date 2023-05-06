import json
from time import sleep

import dramatiq
from apscheduler.schedulers.background import BackgroundScheduler
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from app.config import DefaultSettings
from app.db import DBManager, EventStatus, sql_complete, sql_delete, sql_underway
from app.mq import MQEventType, MQManager


settings = DefaultSettings()
rabbitmq_broker = RabbitmqBroker(url=settings.rabbitmq_uri, confirm_delivery=True)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def event_change_underway():
    mqmanager = MQManager()
    dbmanager = DBManager()
    rows = dbmanager.execute(sql_underway)
    if not rows:
        return
    id_list = [r[0] for r in rows]
    mqmanager.publish_json(
        "events", json.dumps({"status": EventStatus.underway.value, "events": id_list}), MQEventType.change
    )


@dramatiq.actor
def event_complete():
    mqmanager = MQManager()
    dbmanager = DBManager()
    rows = dbmanager.execute(sql_complete)
    if not rows:
        return
    data_list = [{"id": id_, "title": title} for id_, title in rows]
    mqmanager.publish_json("events", json.dumps({"events": data_list}), MQEventType.complete)


@dramatiq.actor()
def event_delete():
    mqmanager = MQManager()
    dbmanager = DBManager()
    rows = dbmanager.execute(sql_delete, settings.HANDICAP_HOURS)
    if not rows:
        return
    id_list = [r[0] for r in rows]
    mqmanager.publish_json("events", json.dumps({"events": id_list}), MQEventType.delete)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(event_change_underway.send, "interval", minutes=settings.CRON_FREQUENCY_MINUTES)
    scheduler.add_job(event_complete.send, "interval", minutes=settings.CRON_FREQUENCY_MINUTES)
    scheduler.add_job(
        event_delete.send,
        "interval",
        minutes=settings.CRON_FREQUENCY_MINUTES,
    )
    scheduler.start()
    worker = dramatiq.Worker(rabbitmq_broker)
    worker.start()
    while True:
        sleep(1)
