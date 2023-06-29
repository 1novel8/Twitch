from celery.result import AsyncResult
from django.http import HttpResponse
from .tasks import get_top_10_streams_task, get_statistics_of_stream_task
from .celery import app


def top_10_streams_right_now(request):
    task_id = get_top_10_streams_task.delay()
    return HttpResponse("<h1>answer will be <a href=http://localhost:8000/get_task_result/?task_id="
                        + str(task_id)
                        + "> here </a></h2>")


def get_task_result(request):
    task_id = request.GET.get('task_id', 0)
    res = AsyncResult(id=task_id, app=app)
    result = res.get()
    return HttpResponse(result)


def get_statistics_of_stream(request):
    stream_id = request.GET.get('stream_id', 0)
    task_id = get_statistics_of_stream_task.delay(stream_id=stream_id)
    return HttpResponse("<h1>answer will be <a href=http://localhost:8000/get_task_result/?task_id="
                        + str(task_id)
                        + "> here </a></h2>")



