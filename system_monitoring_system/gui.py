import PySimpleGUI as sg
import core
import keyring

def layout(settings):
    global g
    cpu_dict = g.cpu()
    memory_dict = g.memory()
    networks = g.network()
    storages = g.storage()
    swap_dict = g.swap()
    users = g.users()
    main_menu = [
        [sg.Text("Overall Usage Summary - ", font=('Montserrat', 10, 'bold'))],
        [sg.Text("Operating System: ", font=('Montserrat', 10, 'bold')), sg.Text(g.os())],
        [sg.Text("Uptime: ", font=('Montserrat', 10, 'bold')), sg.Text("{} seconds".format(g.uptime()))],
        
        
        [sg.Text("\nCPU - ", font=('Montserrat', 10, 'bold'))], 
        [sg.Text("Load Average: ", font=('Montserrat', 10, 'bold')), sg.Text('{}  {}  {}'.format(cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2]))],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],

        [sg.Text("User: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['user']))],
        [sg.Text("System: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['system']))],
        [sg.Text("Idle: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['idle']))],
        [sg.Text("I/O Wait: ", font=('Montserrat', 10, 'bold')), sg.Text('{} %'.format(cpu_dict['iowait']))],
        [sg.Text("Cores: ", font=('Montserrat', 10, 'bold')), sg.Text('{}'.format(cpu_dict['num_cores']))],
        [sg.Text("Total", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['total']))],
        [sg.Text("Used: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['used_incl']))],
        [sg.Text("Free: ", font=('Montserrat', 10, 'bold')), sg.Text('{:,} Bytes'.format(memory_dict['free'])  )],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],

        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        [sg.Text("", font=('Montserrat', 10, 'bold')), sg.Text()],
        # 'User: {} %'.format(cpu_dict['user'])
        # 'System: {} %'.format(cpu_dict['system'])
        # 'Idle: {} %'.format(cpu_dict['idle'])
        # 'I/O Wait: {} %'.format(cpu_dict['iowait'])
        # 'Cores: {}'.format(cpu_dict['num_cores'])
        # 'Total: {:,} Bytes'.format(memory_dict['total'])
        # 'Used: {:,} Bytes'.format(memory_dict['used_incl'])
        # 'Free: {:,} Bytes'.format(memory_dict['free'])  
        # for network_dict in networks:
        #     text = 'Interface: {}'.format(network_dict['interface'])
        #     text = 'IP: {}'.format(network_dict['ip'])
        # for storage_dict in storages:
        #     text = 'Device: {}'.format(storage_dict['device'])
        #     text = 'Mounted: {}'.format(storage_dict['mountpoint'])
        #     text = 'Total: {:,} Bytes'.format(storage_dict['total'])
        #     text = 'Used: {:,} Bytes ({}%)'.format(storage_dict['used'], storage_dict['percent'])
        #     text = 'Free: {:,} Bytes'.format(storage_dict['free'])
        # 'Total: {:,} Bytes'.format(swap_dict['total'])
        # 'Used: {:,} Bytes ({}%)'.format(swap_dict['used'], swap_dict['percent'])
        # 'Free: {:,} Bytes'.format(swap_dict['free'])
        # 'Swapped in: {:,} Bytes'.format(swap_dict['sin'])
        # 'Swapped out: {:,} Bytes'.format(swap_dict['sout'])

        # for user_dict in users:
        #     text = 'Name: {}'.format(user_dict['name'])
        #     text = 'Session started: {}'.format(user_dict['sess_started'])
        #     text = 'Host: {}'.format(user_dict['host'])
        
        [
            sg.Button("Generate report"),
            sg.Button("Send report as email",),
        ],
    ]
    cpu_menu = [
        [sg.Text("Its the cpu menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]
    memory_menu = [
        [sg.Text("Its the memory menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]
    process_menu = [
        [sg.Text("Its the process menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]
    storage_menu = [
        [sg.Text("Its the storage menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]
    network_menu = [
        [sg.Text("Its the network menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]
    misc_menu = [
        [sg.Text("Its the miscellanous menu")],
        [sg.Button("Generate report"), sg.Button("Send report as email")],
    ]

    # names = settings.get("names", ["None"])
    # email = settings.get("email", ["None"])
    
    # name_email = [n+" - "+e for n, e in zip(names, email)]

    # settings.set("name-email", name_email)

    name_email = [n+' - '+e for n, e in settings.get("email", ["None"]).items()]
    print(name_email)
    settings = [
        [sg.Text("Its the settings menu")],
        [sg.Text("Current name(s) - email(s): "), sg.Listbox(
            name_email, key="-email-", size=(100, 5), enable_events=True)],
        [
            sg.Button("Set notification limit"),
            sg.Button("Change record"),
            sg.Button("Delete record"),
            sg.Button("Add record"),
            sg.Button("Change password"),
        ],
    ]

    layout = [
        [sg.T("")],
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Main Menu", main_menu),
                        sg.Tab("CPU Menu", cpu_menu),
                        sg.Tab("Memory Menu", memory_menu),
                        sg.Tab("Process Menu", process_menu),
                        sg.Tab("Storage Menu", storage_menu),
                        sg.Tab("Network Menu", network_menu),
                        sg.Tab("Misc Menu", misc_menu),
                        sg.Tab("Settings Menu", settings),
                    ]
                ],
                border_width=5,
                pad=100,
                enable_events=True,
            )
        ],
    ]

    window = sg.Window(
        "System Monitoring System", layout, size=(1000, 800),
        element_justification="c"
    )
    # window["abc"].Widget.configure(highlightcolor='red',
    # highlightthickness=2)
    return window


def authenticate(settings):
    password = keyring.get_password('sms_password', 'Adminstrator')
    if password is None:
        layout = [
            [sg.Text("Enter NEW Administrator password:")],
            [sg.InputText()],
            [sg.Button("Apply"), sg.Button("Exit")],
        ]
        window = sg.Window("NEW password", layout, finalize=True, modal=True)
        event, values = window.read()
        keyring.set_password('sms_password', 'Adminstrator', values[0])
        window.close()
        return True    
    else:
        auth = False
        layout = [
            [sg.Text("Enter Administrator password:")],
            [sg.InputText()],
            [sg.Button("Authenticate"), sg.Button("Exit")],
        ]
        window = sg.Window(
            "Authenticate as administrator", layout, finalize=True, modal=True
        )
        while True:
            event, values = window.read()

            if (values[0] != password) or event in (
                "Exit",
                sg.WIN_CLOSED,
            ):
                sg.popup(
                    "Error in Authentication, taking back to main menu.",
                    title="Authentication error",
                )
                auth = False
                break

            if values[0] == password:
                sg.popup(
                    "You can now access the settings menu.",
                    title="Authentication successful",
                )
                auth = True
                break
        window.close()
        return auth


def change_record(val, settings):
    layout = [
        [sg.Text("Enter the new name: ")],
        [sg.InputText()],
        [sg.Text("Enter the new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change record", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            name_email[:] = [values[0]+" - "+values[1] if x == val[0] else x for x in name_email]
            settings.set("name-email", name_email)
            sg.popup("Record changed successfully")
            break
    window.close()


def add_record(settings):
    layout = [        
        [sg.Text("Enter the new name: ")],
        [sg.InputText()],
        [sg.Text("Enter a new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Add record", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            name_email.append(values[0]+" - "+values[1])
            settings.set("name-email", name_email)
            sg.popup("Record added successfully")
            break
    window.close()


def delete_record(values, settings):
    name_email.remove(values[0])
    settings.set("name-email", name_email)
    sg.popup("The selected record has been deleted.", title="Record deleted")


def change_password(settings):
    layout = [
        [sg.Text("Enter new password:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change Password", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            keyring.set_password('sms_password', 'Adminstrator', values[0])
            sg.popup("Password changed successfully")
            break

    window.close()


def main():
    auth = False

    window = layout(settings)

    while True:
        event, values = window.read()
        # print(values[0])

        if event == sg.WIN_CLOSED:
            break

        if values[0] == "Settings Menu":
            if not auth:
                auth = authenticate(settings)
                if not auth:
                    window.Element("Main Menu").select()

        if event == "Change password":
            change_password(settings)

        if event == "Add record":
            add_record(settings)
            window["-email-"].update(name_email)
            window.refresh()

        if event == "Change record" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                     title="No email selected")
        elif event == "Change record" and values['-email-']:
            change_record(values['-email-'], settings)
            window["-email-"].update(name_email)
            window.refresh()

        if event == "Delete record" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                     title="No email selected")
        elif event == "Delete record" and values['-email-']:
            delete_record(values['-email-'], settings)
            window["-email-"].update(name_email)
            window.refresh()
    window.refresh()
            # print('lalala')
    window.close()


if __name__ == "__main__":
    g = core.Get()

    sg.theme("SandyBeach")
    sg.set_options(font=('Montserrat', 10))

    settings = sg.UserSettings(filename="./settings.json")
    name_email = settings.get("name-email", ["None"])
    main()
