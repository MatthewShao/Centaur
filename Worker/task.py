from celery import Celery, Task

celery = Celery('task')
celery.config_from_object('config')

def load_scripts():
    # 1. List scripts on Server.
    # 2. Download scripts and save in the form of dict
    pass


def run(self, flow):
    print flow

# load task in this way. Create the task class dynamically
d = {'a':None, 'b':None, 'c':None}
for k in d.iterkeys():
    d[k] = type(k, (Task,), {'name':'task.'+k, 'run':run})

print d