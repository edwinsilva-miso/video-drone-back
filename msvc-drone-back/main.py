#!/usr/bin/env python3
from apscheduler.schedulers.background import BackgroundScheduler

from config import configuration
from src.consumer.VideoStatusConsumer import pull_next_message
from src.initialize import init_app

configuration = configuration['production']

scheduler = BackgroundScheduler()
scheduler.add_job(func=pull_next_message, trigger='interval', seconds=13, max_instances=1)

app = init_app(configuration)

with app.app_context():
    scheduler.start()
