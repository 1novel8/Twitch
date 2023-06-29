import asyncio
from datetime import datetime
import pytz

from motor.motor_asyncio import AsyncIOMotorClient

tz = pytz.timezone('Europe/Minsk')

# new_dict = {'stream_id': stream['id'],
#             'game_name': stream['game_name'],
#             'started_at': stream['started_at'],
#             'viewer_count': stream['viewer_count'],
#             'user_id': stream['user_id'],
#             'user_login': stream['user_login'],
#             'user_name': stream['user_name'],


class DatabaseService:

    async def update_data(self, stream_data: dict, mongo_client: AsyncIOMotorClient):
        await asyncio.gather(*(self._update_data_thread(data, mongo_client) for data in stream_data))

    async def get_stream_data(self, stream_id: int, mongo_client: AsyncIOMotorClient):
        if await self._stream_exist(stream_id=stream_id, mongo_client=mongo_client):
            return await mongo_client.streams.find_one({'_id': stream_id})
        else:
            return None

    async def get_user_data(self, user_id: int, mongo_client: AsyncIOMotorClient):
        if await self._user_exist(user_id=user_id, mongo_client=mongo_client):
            return await mongo_client.users.find_one({'_id': user_id})
        else:
            return None

    @staticmethod
    async def get_all_users(mongo_client: AsyncIOMotorClient):
        users = await mongo_client.users.find().to_list(100)
        return users

    @staticmethod
    async def get_current_user_streams(user_id: int, mongo_client: AsyncIOMotorClient):
        return await mongo_client.streams.find({'user_id': user_id}).to_list(100)

    async def _update_data_thread(self, data: dict, mongo_client: AsyncIOMotorClient):
        if not await self._stream_exist(data['stream_id'], mongo_client=mongo_client):
            await self._create_stream(data={'_id': data['stream_id'],
                                            'user_id': data['user_id'],
                                            'game_name': data['game_name'],
                                            'started_at': data['started_at'],
                                            'viewers': [{
                                                'count': data['viewer_count'],
                                                'time': datetime.now()
                                            }]},
                                      mongo_client=mongo_client)
        else:
            await self._update_stream(stream_id=data['stream_id'],
                                      new_viewer_count=data['viewer_count'],
                                      mongo_client=mongo_client)

        if not await self._user_exist(user_id=data['user_id'],
                                      mongo_client=mongo_client):
            await self._create_user(data={'_id': data['user_id'],
                                          'user_name': data['user_name'],
                                          'user_login': data['user_login'],
                                          'streams_id': [data['stream_id']]},
                                    mongo_client=mongo_client)
        else:
            await self._update_user(user_id=data['user_id'],
                                    new_stream_id=data['stream_id'],
                                    mongo_client=mongo_client)

    @staticmethod
    async def _create_user(data: dict, mongo_client: AsyncIOMotorClient):
        await mongo_client.users.insert_one(data)

    @staticmethod
    async def _create_stream(data: dict, mongo_client: AsyncIOMotorClient):
        await mongo_client.streams.insert_one(data)

    @staticmethod
    async def _update_user(user_id: int, new_stream_id: int, mongo_client: AsyncIOMotorClient):
        streams_future = await mongo_client.users.find_one({'_id': user_id})
        streams = streams_future['streams_id']
        if new_stream_id not in streams:
            mongo_client.users.update_one({'_id': user_id}, {'$push': {'streams_id': new_stream_id}})

    @staticmethod
    async def _update_stream(stream_id: int, new_viewer_count: int, mongo_client: AsyncIOMotorClient):
        mongo_client.streams.update_one({'_id': stream_id},
                                        {'$push': {
                                            'viewers': {
                                                'count': new_viewer_count,
                                                'time': datetime.now()
                                            }
                                        }})

    @staticmethod
    async def _user_exist(user_id: int, mongo_client: AsyncIOMotorClient):
        if await mongo_client.users.find_one({'_id': user_id}):
            return True
        else:
            return False

    @staticmethod
    async def _stream_exist(stream_id: int, mongo_client: AsyncIOMotorClient):
        if await mongo_client.streams.find_one({'_id': stream_id}):
            return True
        else:
            return False

