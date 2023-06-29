import uvicorn
from fastapi import FastAPI
from fastapi_ms.api.views import router
from fastapi_ms.settings import client
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.state.mongo_client = client

app.include_router(router)

app.mount("/static", StaticFiles(directory="fastapi_ms/static"), name='static')

if __name__ == '__main__':
    uvicorn.run(app)


