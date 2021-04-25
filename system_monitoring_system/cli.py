import core
from exceptions import ArgumentError
import getpass
import json
import keyring
import os
import report


def summary():
    """
    Display a summary of System usage data
    """
    g = core.Get()

    text = 'OS: {} \t Uptime: {}'.format(g.os(), g.uptime())
    print(text)

    # CPU data
    text = '\nCPU:-'
    print(text)
    cpu_dict = g.cpu()
    if os.name == 'nt':
        text = 'User: {} % \t System: {} % \t Idle: {} %'.format(
            cpu_dict['idle'], cpu_dict['user'], cpu_dict['system'])
        print(text)
        text = 'Cores: {}'.format(cpu_dict['num_cores'])
        print(text)
    else:
        text = 'Load Average: {} {} {} \t User: {} % \t System: {} %'.format(
            cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2], cpu_dict['user'], cpu_dict['system'])
        print(text)
        text = 'Idle: {} % \t I/O Wait: {} % \t Cores: {}'.format(
            cpu_dict['idle'], cpu_dict['iowait'], cpu_dict['num_cores'])
        print(text)

    # Memory data
    text = '\nMemory:-'
    print(text)
    memory_dict = g.memory()
    text = 'Total: {:,} Bytes \t Used: {:,} Bytes \t Free: {:,} Bytes'.format(
        memory_dict['total'], memory_dict['used_incl'], memory_dict['free'])
    print(text)

    # Network data
    text = '\nNetwork:-'
    print(text)
    networks = g.network()
    for network_dict in networks:
        if os.name == 'nt':
            text = 'Interface: {}'.format(network_dict['interface'])
            print(text)
        else:
            text = 'Interface: {} \t IP: {}'.format(
                network_dict['interface'], network_dict['ip'])
            print(text)

    # Storage data
    text = '\nStorage:-'
    print(text)
    storages = g.storage()
    for storage_dict in storages:
        text = 'Device: {} \t Mounted: {} \t Total: {:,} Bytes'.format(
            storage_dict['device'], storage_dict['mountpoint'], storage_dict['total'])
        print(text)
        text = 'Used: {:,} Bytes ({}%) \t Free: {:,} Bytes'.format(
            storage_dict['used'], storage_dict['percent'], storage_dict['free'])
        print(text)

    # Swap data
    text = '\nSwap:-'
    print(text)
    swap_dict = g.swap()
    text = 'Total: {:,} Bytes \t Used: {:,} Bytes ({}%) \t Free: {:,} Bytes'.format(
        swap_dict['total'], swap_dict['used'], swap_dict['percent'], swap_dict['free'])
    print(text)
    text = 'Swapped in: {:,} Bytes \t Swapped out: {:,} Bytes'.format(
        swap_dict['sin'], swap_dict['sout'])
    print(text)

    # Users data
    text = '\nUsers:-'
    print(text)
    users = g.users()
    for user_dict in users:
        text = 'Name: {} \t Session started: {} \t Host: {}'.format(
            user_dict['name'], user_dict['sess_started'], user_dict['host'])
        print(text)


def cpu():
    """
    Display detailed CPU usage data
    """
    g = core.Get()

    text = 'CPU Usage:\n'
    print(text)
    cpu_dict = g.cpu()
    if os.name == 'nt':
        text = 'User: {} % \t System: {} % \t Idle: {} %'.format(
            cpu_dict['idle'], cpu_dict['user'], cpu_dict['system'])
        print(text)
        counter = 1
        for cpu_core in cpu_dict['cores']:
            print()
            text = 'Core {}:-'.format(counter)
            print(text)
            text = 'User: {} % \t System: {} % \t Idle: {} %'.format(
                cpu_core['user'], cpu_core['system'], cpu_core['idle'])
            print(text)
            counter += 1
    else:
        text = 'Load Average: {} {} {} \t User: {} % \t System: {} %'.format(
            cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2], cpu_dict['user'], cpu_dict['system'])
        print(text)
        text = 'Idle: {} % \t I/O Wait: {} %'.format(
            cpu_dict['idle'], cpu_dict['iowait'])
        print(text)
        counter = 1
        for cpu_core in cpu_dict['cores']:
            print()
            text = 'Core {}:-'.format(counter)
            print(text)
            text = 'User: {} % \t System: {} % \t Idle: {} %'.format(
                cpu_core['user'], cpu_core['system'], cpu_core['idle'])
            print(text)
            text = 'I/O Wait: {} %'.format(cpu_core['iowait'])
            print(text)
            counter += 1


def memory():
    """
    Display detailed Memory usage data
    """
    g = core.Get()

    text = 'Memory Usage:\n'
    print(text)
    memory_dict = g.memory()
    text = 'Total: {:,} Bytes \t Available: {:,} Bytes \t Used(excl. Cache & buffer): {:,} Bytes ({}%)'.format(
        memory_dict['total'], memory_dict['available'], memory_dict['used_excl'], memory_dict['percent'])
    print(text)
    text = 'Used (incl, Cache & Buffer): {:,} Bytes \t Free: {:,} Bytes'.format(
        memory_dict['used_incl'], memory_dict['free'])
    print(text)


def process():
    """
    Display detailed Process usage data
    """
    g = core.Get()

    text = 'Process Usage:'
    print(text)
    processes = g.process()
    for process_dict in processes:
        print()
        text = 'PID: {} \t Name: {} \t User: {}'.format(
            process_dict['pid'], process_dict['name'], process_dict['user'])
        print(text)
        text = 'Status: {} \t Created: {} seconds since the epoch \t Memory: {} %'.format(
            process_dict['status'], process_dict['created'], process_dict['memory'])
        print(text)
        text = 'CPU: {} %'.format(process_dict['cpu'])
        print(text)


def storage():
    """
    Display detailed Storage usage data
    """
    g = core.Get()

    text = 'Storage Usage:'
    print(text)
    storages = g.storage()
    for storage_dict in storages:
        print()
        text = 'Device: {} \t Mounted: {} \t Type: {}'.format(
            storage_dict['device'], storage_dict['mountpoint'], storage_dict['fstype'])
        print(text)
        text = 'Options: {} \t Total: {:,} Bytes \t Used: {:,} Bytes ({}%)'.format(
            storage_dict['options'], storage_dict['total'], storage_dict['used'], storage_dict['percent'])
        print(text)
        text = 'Free: {:,} Bytes'.format(storage_dict['free'])
        print(text)


def network():
    """
    Display detailed Network usage data
    """
    g = core.Get()

    text = 'Network Usage:'
    print(text)
    networks = g.network()
    if os.name == 'nt':
        for network_dict in networks:
            print()
            text = 'Interface: {} \t Bytes sent: {} \t Bytes received: {}'.format(
                network_dict['interface'], network_dict['bytes_sent'], network_dict['bytes_recv'])
            print(text)
            text = 'Packets sent: {} \t Packets received: {} \t Errors in: {}'.format(
                network_dict['packets_sent'], network_dict['packets_recv'], network_dict['errin'])
            print(text)
            text = 'Errors out: {} \t Dropped in: {} \t Dropped out: {}'.format(
                network_dict['errout'], network_dict['dropin'], network_dict['dropout'])
            print(text)
    else:
        for network_dict in networks:
            print()
            text = 'Interface: {} \t IP: {} \t Bytes sent: {}'.format(
                network_dict['interface'], network_dict['ip'], network_dict['bytes_sent'])
            print(text)
            text = 'Bytes received: {} \t Packets sent: {} \t Packets received: {}'.format(
                network_dict['bytes_recv'], network_dict['packets_sent'], network_dict['packets_recv'])
            print(text)
            text = 'Errors in: {} \t Errors out: {} \t Dropped in: {}'.format(
                network_dict['errin'], network_dict['errout'], network_dict['dropin'])
            print(text)
            text = 'Dropped out: {}'.format(network_dict['dropout'])
            print(text)

    speed_dict = core.test_speed()

    text = '\nDownload speed: {} \t Upload speed: {}'.format(
        speed_dict['down_speed'], speed_dict['up_speed'])
    print(text)


def misc():
    """
    Display Miscellaneous usage data
    """
    g = core.Get()

    text = 'Miscellaneous Usage:\n'
    print(text)
    text = 'OS: {} \t Uptime: {} seconds\n'.format(g.os(), g.uptime())
    print(text)

    text = 'Users:-'
    print(text)
    users = g.users()
    for user_dict in users:
        print()
        text = 'Name: {} \t Session started: {} \t Host: {}'.format(
            user_dict['name'], user_dict['sess_started'], user_dict['host'])
        print(text)

    text = '\nSwap:-\n'
    print(text)
    swap_dict = g.swap()
    text = 'Total: {:,} Bytes \t Used: {:,} Bytes ({}%) \t Free: {:,} Bytes'.format(
        swap_dict['total'], swap_dict['used'], swap_dict['percent'], swap_dict['free'])
    print(text)
    text = 'Swapped in: {:,} Bytes \t Swapped out: {:,} Bytes'.format(
        swap_dict['sin'], swap_dict['sout'])
    print(text)


def show_limit():
    """
    Display notification limits
    """
    settings_file = open(os.path.join(
        os.path.expanduser('~'), '.sms/settings.json'))
    settings = json.load(settings_file)
    settings_file.close()

    for resource, value in settings['limit'].items():
        print('{} - {}'.format(resource, value))


def update_limit(resource, limit):
    """
    Update notification limits
    """
    if resource not in ['cpu', 'memory', 'storage', 'swap']:
        msg = """
Invalid resource name entered.

Valid resource names are:
 - cpu
 - memory
 - storage
 - swap
"""
        raise ArgumentError(msg)

    password = keyring.get_password('sms_password', 'Administrator')
    if password == None:
        print('No Password set.\nSet a new password using `sms --update-password`.')
        return

    user_password = getpass.getpass()
    if user_password != password:
        print('\nWrong Password entered')
        return

    if limit >= 100 or limit <= 0:
        msg = """
Invalid limit entered.

Limit must be between 0 and 100.
"""
        raise ArgumentError(msg)

    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    settings['limit'][resource] = limit

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def show_email():
    """
    Display saved name and email address
    """
    settings_file = open(os.path.join(
        os.path.expanduser('~'), '.sms/settings.json'))
    settings = json.load(settings_file)
    settings_file.close()

    for email, name in settings['email'].items():
        print('{} - {}'.format(name, email))


def update_email(action, *args):
    if action not in ['add', 'modify', 'remove']:
        msg = """
Invalid action entered.

Valid actions are:
 - add
 - modify
 - remove
"""
        raise ArgumentError(msg)

    password = keyring.get_password('sms_password', 'Administrator')
    if password == None:
        print('No Password set.\nSet a new password using `sms --update-password`.')
        return

    user_password = getpass.getpass()
    if user_password != password:
        print('\nWrong Password entered')
        return

    if action == 'add':
        if len(args) != 2:
            raise ArgumentError
        add_email(*args)
    elif action == 'modify':
        if len(args) != 4:
            raise ArgumentError
        modify_email(*args)
    elif action == 'remove':
        if len(args) != 1:
            print(args)
            raise ArgumentError
        remove_email(*args)


def add_email(name, email):
    """
    Add name and email address
    """
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    settings['email'][email] = name

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def modify_email(old_name, old_email, new_name, new_email):
    """
    Modify saved name and email address
    """
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    if old_email not in settings['email']:
        msg = 'email provided does not exist.'
        raise ArgumentError(msg)

    del settings['email'][old_email]

    settings['email'][new_email] = new_name

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def remove_email(email):
    """
    Remove name and email address
    """
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    if email not in settings['email']:
        msg = 'email provided does not exist.'
        raise ArgumentError(msg)

    del settings['email'][email]

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def update_password():
    """
    Modify administrator password
    """
    old_password = keyring.get_password('sms_password', 'Administrator')
    if old_password != None:
        user_old_password = getpass.getpass(prompt='Old Password: ')
        if user_old_password != old_password:
            print('\nWrong Password entered')
            return

    new_password = getpass.getpass(prompt='New Password: ')
    conf_new_password = getpass.getpass(prompt='Confirm New Password: ')
    if new_password != conf_new_password:
        print('\nPassword Mismatch')
        return

    keyring.set_password('sms_password', 'Administrator', new_password)


def send_email(resource='Summary'):
    """
    Send email to saved email address
    """
    email = input('Google account email: ')
    password = getpass.getpass()
    report.send_email(email, password, resource)

    print('Mail Sent')


if __name__ == '__main__':
    exit()
