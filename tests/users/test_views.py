from project.users.models import User
from unittest import mock
import requests
from flask import url_for
from project.users import tasks


def test_pytest_setup(client,db):
    resp = client.get('/users/form/')
    assert resp.status_code == 200

    user = User(username='test',email='test@test.com')
    db.session.add(user)
    db.session.commit()
    assert user.id

def test_view_with_eager_mode(client,db,config,monkeypatch):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests,'post',mock_requests_post)

    config.update(CELERY_TASK_ALWAYS_EAGER=True)

    response = client.get(url_for('users.user_subscribe'))
    assert response.status_code == 200

    user_name = 'michaelyin'
    user_email = f'{user_name}@accordbox.com'
    response = client.post(url_for('users.user_subscribe'),
                           data={'email': user_email,
                                 'username': user_name},
                           )

    assert response.status_code == 200
    assert b'sent task to Celery successfully' in response.data

    mock_requests_post.assert_called_with(
        'https://httpbin.org/delay/5',
        data={'email': user_email}
    )

def test_user_subscribe_view(client, db, monkeypatch, user_factory):
    user = user_factory.build()

    task_add_subscribe = mock.MagicMock(name='task_add_subscribe')
    task_add_subscribe.return_value = mock.MagicMock(task_id='task_id')
    monkeypatch.setattr(tasks.task_add_subscribe,'delay',task_add_subscribe)

    resp = client.get(url_for('users.user_subscribe'))
    assert resp.status_code == 200

    resp = client.post(url_for('users.user_subscribe'),
        data={
            'email': user.email,
            'username': user.username,
        }
    )

    assert resp.status_code == 200

    assert b'sent task to Celery successfully' in resp.data

    user = User.query.filter_by(username=user.username).first()
    task_add_subscribe.assert_called_with(
        user.id
    )