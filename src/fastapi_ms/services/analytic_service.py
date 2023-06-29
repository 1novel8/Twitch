import matplotlib.pyplot as plt
import numpy as np


class AnalyticService:
    @staticmethod
    def create_plot(data: dict):
        fig, ax = plt.subplots()

        ax.set_xlabel('time')
        ax.set_ylabel('Viewers')

        x = []
        y = []
        max_viewers = 0
        time_of_max = '0'
        for it in data['viewers']:
            if it['count'] > max_viewers:
                max_viewers = it['count']
                time_of_max = str(it['time'].hour)+':' + str(it['time'].minute)
            y.append(it['count'])
            if it['time'].minute < 10:
                x.append(str(it['time'].hour) + ':' + '0' + str(it['time'].minute))
            else:
                x.append(str(it['time'].hour)+':' + str(it['time'].minute))

        ax.set_title('Game name:' + str(data['game_name']) + '\n'
                     + 'Started at:' + str(data['started_at']) + '\n'
                     + 'Pick: ' + str(max_viewers)
                     + ' at:' + time_of_max, fontsize=9)

        ax.set_yticks(np.arange(0, max_viewers*1.5, max_viewers/15))
        plt.xticks(rotation=90)
        ax.grid()
        ax.plot(x, y, marker='.')
        fig.savefig('fastapi_ms/static/'+str(data['_id'])+'.png')

