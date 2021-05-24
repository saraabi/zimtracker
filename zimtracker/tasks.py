import time
import os

from celery import shared_task
from django.apps import apps

from django_zimtracker.celery import app

from .functions import update_vessels

@shared_task
def task_update_vessels():
    update_vessels()