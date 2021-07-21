# updater.py
# The AHJ Registry
# March, 2021

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from ScheduledTasks import editTasks
from django.conf import settings


def start():
    scheduler = BackgroundScheduler()
    # if settings.DEBUG:
    #     scheduler.add_job(editTasks.test_proc, 'interval', seconds=60)
    scheduler.add_job(editTasks.edits_take_effect, 'cron', hour=3, jitter=10)
    scheduler.add_job(editTasks.deactivate_expired_api_tokens, 'cron', hour=3, jitter=10)
    scheduler.start()
