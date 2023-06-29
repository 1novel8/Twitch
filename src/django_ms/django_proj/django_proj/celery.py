import json
import os

import requests
from celery import Celery
from requests import HTTPError

from django_proj.tasks import update_data_every_5_min

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_proj.settings')

app = Celery('django_proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update-data": {
        "task": "django_proj.tasks.update_data_every_5_min",
        "schedule": 300.0
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task()
def get_stats(stream_id):
    body = {"stream_id": stream_id}
    body = json.dumps(body)
    try:
        response = requests.get(url='http://fastapi_host:8080/twitch/analytics/', body=body)
    except HTTPError:
        return response.status_code
    else:
        return response.request.body
