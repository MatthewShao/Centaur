from celery import Celery

celery = Celery('task')
celery.config_from_object('config')

