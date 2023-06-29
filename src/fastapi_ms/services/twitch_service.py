from twitchAPI import Twitch


class TwitchService:
    async def get_top_streams(self):
        twitch = await Twitch('2z365foos8mww2qlmq5214gjncx91j', 'fc4qbm5z5f8oukl0o2e5mvjokw54rc')
        streams = twitch.get_streams(language='ru', first=11)
        top_streams = []

        async for stream in streams:
            top_streams.append(await self._filter_data_of_stream(stream.to_dict()))
            if len(top_streams) == 10:
                return top_streams

    @staticmethod
    async def _filter_data_of_stream(stream: dict):
        new_dict = {'stream_id': int(stream['id']),
                    'game_name': stream['game_name'],
                    'started_at': stream['started_at'],
                    'viewer_count': int(stream['viewer_count']),
                    'user_id': int(stream['user_id']),
                    'user_login': stream['user_login'],
                    'user_name': stream['user_name']}
        return new_dict


