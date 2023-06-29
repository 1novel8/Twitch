FROM python:3.10.5-slim

WORKDIR ./src

COPY ./requirements.txt ./requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . ./fastapi_ms

EXPOSE 8080

CMD ["uvicorn", "fastapi_ms.main:app", "--host", "0.0.0.0", "--port", "8080"]
