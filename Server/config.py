# celery config
BROKER_URL = "amqp://celery:121131141@208.51.63.113:5672/centaur"
# CELERY_RESULT_BACKEND = "db+postgresql://centaur:cent4uri$c00l@208.51.63.113/celery"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# db_config
db_host = "localhost"
db_user = "test"
db_pass = "test"
db_name = "centaur"
# flask config

SERVER_URL = "http://127.0.0.1:5000"
CSRF_ENABLED = True
SECRET_KEY = '252c0cca000c3674b8ef7a2b8ecd409695aac370'