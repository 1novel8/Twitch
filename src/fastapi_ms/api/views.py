from os.path import isfile

from fastapi import APIRouter, Depends
from starlette.requests import Request
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import guess_type, Response
from fastapi.responses import RedirectResponse

from fastapi_ms.services.analytic_service import AnalyticService
from fastapi_ms.services.twitch_service import TwitchService
from fastapi_ms.services.db_service import DatabaseService

router = APIRouter(prefix='/twitch')


@router.get('/top_10_streams_right_now', response_model=list)
async def get_top_10_streams_rn(service: TwitchService = Depends()):
    top_streams = await service.get_top_streams()
    return top_streams


@router.get('/update_data', response_model=str)
async def update_data(request: Request,
                      db: DatabaseService = Depends(),
                      service: TwitchService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    top_streams = await service.get_top_streams()
    await db.update_data(top_streams, mongo_client=mongo_client)
    return 'Updated'


@router.get('/get_100_users', response_model=list)
async def get_100_users(request: Request,
                        db: DatabaseService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    return await db.get_all_users(mongo_client=mongo_client)


@router.get('/get_100_streams', response_model=list)
async def get_100_streams(request: Request,
                          db: DatabaseService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    return await db.get_all_users(mongo_client=mongo_client)


@router.get('/get_stream_info', response_model=dict)
async def get_stream_info(request: Request,
                          stream_id: int,
                          db: DatabaseService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    return await db.get_stream_data(stream_id=stream_id, mongo_client=mongo_client)


@router.get('/get_user_info', response_model=dict)
async def get_user_info(request: Request,
                        user_id: int,
                        db: DatabaseService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    return await db.get_user_data(user_id=user_id, mongo_client=mongo_client)


@router.post('/get_current_user_streams', response_model=list)
async def get_current_user_streams(request: Request,
                                   user_id: int,
                                   db: DatabaseService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    return await db.get_current_user_streams(user_id=user_id, mongo_client=mongo_client)


@router.get('/get_statistics_of_stream')
async def get_statistics_of_stream(request: Request,
                                   stream_id: int,
                                   db: DatabaseService = Depends(),
                                   analytics: AnalyticService = Depends()):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["twitch_db"]
    stream_data = await db.get_stream_data(stream_id=stream_id, mongo_client=mongo_client)
    if stream_data:
        analytics.create_plot(data=stream_data)
        return RedirectResponse('http://localhost:8080/static/' + str(stream_data['_id']) + '.png')
    else:
        return 'Wrong stream_id'


@router.get("/static/{filename}")
async def get_image(filename):
    filename = './static/' + filename

    if not isfile(filename):
        return Response(status_code=404)

    with open(filename) as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)
