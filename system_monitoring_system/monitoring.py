import core
import json
import os
from plyer import notification
import time
import warnings


def start():
    try:
        warnings.filterwarnings('ignore')
        while True:
            g = core.Get()

            settings_file = open(os.path.join(
                os.path.expanduser('~'), '.sms/settings.json'))
            limit = json.load(settings_file)['limit']
            settings_file.close()

            if 'cpu' in limit:
                cpu_usage = g.cpu_overall()
                if cpu_usage >= limit['cpu']:
                    message = 'CPU limit reached\nCurrent CPU usage is {} %\nMaximum allowed limit is set at {} %'.format(
                        cpu_usage, limit['cpu'])
                    notification.notify(
                        title='System Monitoring System', message=message)

            if 'memory' in limit:
                memory_usage = g.memory()['percent']
                if memory_usage >= limit['memory']:
                    message = 'Memory limit reached\nCurrent Memory usage is {} %\nMaximum allowed limit is set at {} %'.format(
                        memory_usage, limit['memory'])
                    notification.notify(
                        title='System Monitoring System', message=message)

            if 'storage' in limit:
                storages = g.storage()
                for storage in storages:
                    storage_usage = storage['percent']
                    if storage_usage >= limit['storage']:
                        message = 'Storage limit reached for device {}\nCurrent Storage usage is {} %\nMaximum allowed limit is set at {} %'.format(
                            storage['device'], storage_usage, limit['storage'])
                        notification.notify(
                            title='System Monitoring System', message=message)

            if 'swap' in limit:
                swap_usage = g.swap()['percent']
                if swap_usage >= limit['swap']:
                    message = 'Swap limit reached\nCurrent Swap usage is {} %\nMaximum allowed limit is set at {} %'.format(
                        swap_usage, limit['swap'])
                    notification.notify(
                        title='System Monitoring System', message=message)

            time.sleep(300)

    except KeyboardInterrupt:
        print('\nExiting')


if __name__ == '__main__':
    exit()
