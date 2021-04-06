from exceptions import ArgumentError
import core


def print_main_menu():
    g = core.Get()
    os = g.os()
    print(os)


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
