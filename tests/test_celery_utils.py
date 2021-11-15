import pytest

from project import db
from project.celery_utils import custom_celery_task
from project.users.models import User


# tasks

@custom_celery_task()
def successful_task(user_id):
    user = User.query.get(user_id)
    user.username = 'test'
    db.session.commit()


# tests

def test_custom_celery_task(db, config, user):
    config.update(CELERY_TASK_ALWAYS_EAGER=True)

    successful_task.delay(user.id)

    assert User.query.get(user.id).username == 'test'