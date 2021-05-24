release: python manage.py migrate
web: gunicorn django_zimtracker.wsgi —-log-file -
worker: REMAP_SIGTERM=SIGQUIT celery worker --app django_zimtracker.celery.app --loglevel info