# celery config
BROKER_URL = "amqp://guest:guest@rabbitmq.t0.daoapp.io:61539//"
CELERY_RESULT_BACKEND = 'mongodb://localhost:27017/'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database':'centaur'
}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# db_config
DB_HOST = "localhost"
DB_USER = "test"
DB_PASS = "test"
DB_NAME = "centaur"
# flask config

SERVER_URL = "http://127.0.0.1:5000"
CSRF_ENABLED = True
SECRET_KEY = '252c0cca000c3674b8ef7a2b8ecd409695aac370'