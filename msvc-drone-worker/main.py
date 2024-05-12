#!/usr/bin/env python3
from apscheduler.schedulers.background import BackgroundScheduler

from src.initialize import provide_app
from src.tasks.VideoWorkerConsumer import pull_next_message

scheduler = BackgroundScheduler()
scheduler.add_job(func=pull_next_message, trigger='interval', seconds=13, max_instances=1)

app = provide_app()

with app.app_context():
    scheduler.start()
