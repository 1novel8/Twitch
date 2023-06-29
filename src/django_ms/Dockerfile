FROM python:3.10.5-slim


EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR ./django_ms

COPY requirements.txt ./requirements.txt


RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .