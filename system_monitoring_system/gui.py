import PySimpleGUI as sg


def layout(settings):

    main_menu = [
        [sg.Text("Its the main menu")],
        [
            sg.Button("Generate report"),
            sg.Button(
                "Send report as email",
            ),
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

    email = settings.get("email", "None")
    settings = [
        [sg.Text("Its the settings menu")],
        [sg.Text("Current email(s): "), sg.Listbox(
            email, key="-email-", size=(100, 5), enable_events=True)],
        [
            sg.Button("Set notification limit"),
            sg.Button("Change email"),
            sg.Button("Delete email"),
            sg.Button("Add email"),
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
        "System Monitoring System", layout, size=(900, 700), element_justification="c"
    )
    # window["abc"].Widget.configure(highlightcolor='red', highlightthickness=2)
    return window


def authenticate(settings):
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

        if (values[0] != settings.get("password", "None")) or event in (
            "Exit",
            sg.WIN_CLOSED,
        ):
            sg.popup(
                "Error in Authentication, taking back to main menu.",
                title="Authentication error",
            )
            auth = False
            # print("lulu")
            break

        if values[0] == settings.get("password", "None"):
            sg.popup(
                "You can now access the settings menu.",
                title="Authentication successful",
            )
            auth = True
            # print('aulelele')
            break

    window.close()
    return auth


def change_email(l, settings):
    print(l[0])
    email = settings.get("email", "None")

    layout = [
        [sg.Text("Enter the new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change email", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            email[:] = [values[0] if x == l[0] else x for x in email]
            settings.set("email", email)
            sg.popup("Email changed successfully")
            break
    window.close()


def add_email(settings):
    email = settings.get("email", "None")

    layout = [
        [sg.Text("Enter a new email:")],
        [sg.InputText()],
        [sg.Button("Apply"), sg.Button("Exit")],
    ]
    window = sg.Window("Change email", layout, finalize=True, modal=True)
    while True:
        event, values = window.read()

        if event in ("Exit", sg.WIN_CLOSED):
            break

        elif event == "Apply":
            email.append(values[0])
            settings.set("email", email)
            sg.popup("Email changed successfully")
            break
    window.close()


def delete_email(l, settings):
    email = settings.get("email", "None")
    email.remove(l[0])
    settings.set("email", email)
    sg.popup("The selected email has been deleted.", title="Email deleted")


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
            settings.set("password", values[0])
            sg.popup("Password changed successfully")
            break

    window.close()


def main():
    sg.theme("SandyBeach")
    auth = False
    settings = sg.UserSettings(filename="./settings.json")
    print(settings.full_filename)
    window = layout(settings)

    while True:
        event, values = window.read()
        print(type(event), type(values['-email-']))

        if event == sg.WIN_CLOSED:
            break

        if values[0] == "Settings Menu":
            if not auth:
                auth = authenticate(settings)
                if not auth:
                    window.Element("Main Menu").select()

        if event == "Change password":
            change_password(settings)

        if event == "Add email":
            add_email(settings)
            window["-email-"].update(settings.get("email", "None"))
            window.refresh()

        if event == "Change email" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                     title="No email selected")
        elif event == "Change email" and values['-email-']:
            change_email(values['-email-'], settings)
            window["-email-"].update(settings.get("email", "None"))
            window.refresh()

        if event == "Delete email" and not values['-email-']:
            sg.popup("Select an email from the list and try again!",
                     title="No email selected")
        elif event == "Delete email" and values['-email-']:
            delete_email(values['-email-'], settings)
            window["-email-"].update(settings.get("email", "None"))
            window.refresh()

            # print('lalala')
    window.close()


if __name__ == "__main__":
    main()
