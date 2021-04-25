import os
import json
import shutil


def create_directory():
    path = os.path.join(os.path.expanduser('~'), '.sms')
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)


def create_executable():
    os.system('pip3 install -q pipenv')
    os.system('pipenv install --ignore-pipfile')
    os.system('pipenv run pyinstaller --onefile --name sms --clean --distpath . --log-level ERROR --hidden-import plyer.platforms.win.notification system_monitoring_system/__main__.py')


def add_to_path():
    exec_path = os.path.join(os.path.expanduser('~'), '.sms', 'bin')
    if not os.path.exists(exec_path) or not os.path.isdir(exec_path):
        os.mkdir(exec_path)

    exec_path = os.path.join(exec_path, 'sms.exe')
    shutil.copy('sms.exe', exec_path)

    print('Add the following file in PATH variable to access sms from anywhere.')
    print(exec_path)


def copy_files():
    path = os.path.join(os.path.expanduser('~'), '.sms')
    shutil.copy('./Montserrat-Regular.ttf', path)
    shutil.copy('./Montserrat-Bold.ttf', path)
    shutil.copy('./sms_icon.png', path)


def create_settings():
    path = os.path.join(os.path.expanduser('~'), '.sms', 'settings.json')
    if not os.path.exists(path) or not os.path.isfile(path):
        settings = {'email': {}, 'limit': {'cpu': 75,
                                           'memory': 50, 'storage': 60, 'swap': 80}}
        with open(path, 'w') as f:
            json.dump(settings, f)


def remove_extras():
    shutil.rmtree('build')
    os.remove('sms.spec')


if __name__ == '__main__':
    if os.name == 'nt':
        create_directory()
        create_executable()
        add_to_path()
        copy_files()
        create_settings()
        remove_extras()
    else:
        exit()
