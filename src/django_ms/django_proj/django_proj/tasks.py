import json

from celery import shared_task
import requests
from requests.exceptions import HTTPError


@shared_task
def update_data_every_5_min():
    try:
        response = requests.get(url='http://fastapi_host:8080/twitch/update_data', )
    except HTTPError:
        return response.status_code
    else:
        return response.status_code


@shared_task
def get_top_10_streams_task():
    try:
        response = requests.get(url='http://fastapi_host:8080/twitch/top_10_streams_right_now', )
    except HTTPError:
        return response.status_code
    else:
        return response.text


@shared_task
def get_statistics_of_stream_task(stream_id):
    try:
        response = requests.get(url='http://fastapi_host:8080/twitch/get_statistics_of_stream/', params={'stream_id': stream_id})
    except HTTPError:
        return response.status_code
    else:
        return response.text




