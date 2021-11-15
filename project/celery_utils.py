from celery import current_app as current_celery_app
from celery import Task, shared_task
import functools

def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")

    if not hasattr(celery,'flask_app'):
        celery.flask_app = app
    celery.Task = AppContextTask
    return celery

class AppContextTask(Task):
    def __call__(self, *args, **kwargs):
        with self.app.flask_app.app_context():
            Task.__call__(self,*args,**kwargs)


class custom_celery_task:
    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self,func):
        @functools.wraps(func)
        def wrapper_func(*args,**kwargs):
            #CUSTOM CODE HERE
            return func(*args,**kwargs)
        
        task_func = shared_task(*self.task_args,**self.task_kwargs)(wrapper_func)
        return task_func