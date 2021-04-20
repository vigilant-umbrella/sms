import core
from exceptions import ArgumentError


def print_main_menu():
    g = core.Get()

    text = 'OS: {} \t Uptime: {}'.format(g.os(), g.uptime())
    print(text)

    # CPU data
    text = '\nCPU:-'
    print(text)
    cpu_dict = g.cpu()
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
    text = 'Total: {:,} Bytes \t Used: Used: {:,} Bytes \t Free: {:,} Bytes'.format(
        memory_dict['total'], memory_dict['used_incl'], memory_dict['free'])
    print(text)

    # Network data
    text = '\nNetwork:-'
    print(text)
    networks = g.network()
    for network_dict in networks:
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


def print_cpu():
    pass


def call(args):
    if args[0] == '--summary' or args[0] == '-S':
        print_main_menu()
    elif args[0] == '--cpu' or args[0] == '-c':
        print_cpu()
    else:
        msg = """
        Invalid Arugment Provided

        Correct Arugments Available are:
         o --summary or -S: To display the summary of all the resources of the system.
         o --cpu or -c: To display info regarding the system CPU.
         o --memory or -M: To display info regarding the system memory.
         o --process or -p: To display info regarding the system processes.
         o --storage or -s: To display info regarding the system storage.
         o --network or -n: To display info regarding the system’s network connections.
         o --misc or -m: To display miscellaneous system info.
         o --update-limit <resource-name> <limit>: Updates notification limit for the provided resource.
         o --update-email add <name> <email>: Adds a new email to the email list.
         o --update-email remove <email>: Adds an email from the email list.
         o --update-email modify <old_name> <old_email> <new_name> <new_email>: Updates info regarding an existing email.
         o --update-password: Updates the authentication password.
        """
        raise ArgumentError(msg)


if __name__ == '__main__':
    exit()
