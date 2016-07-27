BROKER_URL = "amqp://guest:guest@rabbitmq.t0.daoapp.io:61539//"
# CELERY_RESULT_BACKEND = 'mongodb//localhost:27017/'
# CELERY_MONGODB_BACKEND_SETTINGS = {
#     'database':'centaur'
# }
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

SERVER = "http://127.0.0.1:5000"
TASK_TIMEOUT = 30