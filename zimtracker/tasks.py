import time
import os

from django.apps import apps

from django_zimtracker.celery import app

from .functions import update_vessels

@app.task
def task_update_vessels():
    update_vessels()