import cli
import fire
import gui
import monitoring
import report
import os
import json
import shutil


def create_sms_folder():
    path = os.path.join(os.path.expanduser('~'), '.sms')

    try:
        if not os.path.exists(path) or not os.path.isdir(path):
            os.mkdir(path)
            shutil.copy('./Montserrat-Regular.ttf', path)
            shutil.copy('./Montserrat-Bold.ttf', path)
            shutil.copy('./sms_icon.png', path)

            path = os.path.join(os.path.expanduser('~'), '.sms', 'settings.json')
            if not os.path.exists(path) or not os.path.isfile(path):
                settings = {'email': {}, 'limit': {'cpu': 75,
                                                'memory': 50, 'storage': 60, 'swap': 80}}
                with open(path, 'w') as f:
                    json.dump(settings, f)
    except PermissionError:
        print('Run sms with sudo for the first time --> sudo sms')


if __name__ == '__main__':
    create_sms_folder()
   
    commands = {
        '--summary': cli.summary,
        '--cpu': cli.cpu,
        '--memory': cli.memory,
        '--process': cli.process,
        '--storage': cli.storage,
        '--network': cli.network,
        '--misc': cli.misc,
        '--show-limit': cli.show_limit,
        '--update-limit': cli.update_limit,
        '--show-email': cli.show_email,
        '--update-email': cli.update_email,
        '--update-password': cli.update_password,
        '--send-email': cli.send_email,
        '--down-report': report.down_report,
        '--start-monitoring': monitoring.start,
        '--gui': gui.main,
        '-S': cli.summary,
        '-c': cli.cpu,
        '-M': cli.memory,
        '-p': cli.process,
        '-s': cli.storage,
        '-n': cli.network,
        '-m': cli.misc,
        '-g': gui.main
    }

    fire.Fire(commands)
