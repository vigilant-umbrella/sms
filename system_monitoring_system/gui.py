import PySimpleGUI as sg


def layout(row, col):
    main_menu = [[sg.Text('Its the main menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email',)]]
    cpu_menu = [[sg.Text('Its the cpu menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    memory_menu = [[sg.Text('Its the memory menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    process_menu = [[sg.Text('Its the process menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    storage_menu = [[sg.Text('Its the storage menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    network_menu = [[sg.Text('Its the network menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    misc_menu = [[sg.Text('Its the miscellanous menu')], [sg.Button(
        'Generate report'), sg.Button('Send report as email')]]
    settings = [[sg.Text('Its the settings menu')], [sg.Button('Set notification limit'), sg.Button(
        'Change email'), sg.Button('Add email'), sg.Button('Change password')]]

    layout = [[sg.T("")],
              [sg.TabGroup(
                  [
                      [sg.Tab('Main Menu', main_menu), sg.Tab('CPU Menu', cpu_menu), sg.Tab('Memory Menu', memory_menu),
                       sg.Tab('Process Menu', process_menu), sg.Tab(
                          'Storage Menu', storage_menu), sg.Tab('Network Menu', network_menu),
                       sg.Tab('Misc Menu', misc_menu), sg.Tab(
                          'Settings Menu', settings),
                       ]
                  ], border_width=5, pad=100, enable_events=True
              )
    ]
    ]

    window = sg.Window('System Monitoring System', layout,
                       size=(900, 700), element_justification='c')
    # window["abc"].Widget.configure(highlightcolor='red', highlightthickness=2)
    return window


def authenticate(settings):
    auth = False
    layout = [[sg.Text('Enter Administrator password:')], [sg.InputText()], [
        sg.Button('Authenticate'), sg.Button('Exit')]]
    window = sg.Window('Authenticate as administrator',
                       layout, finalize=True, modal=True)
    while True:
        event, values = window.read()
        if (values[0] != settings.get('password', None)) or event == "Exit" or event == sg.WIN_CLOSED:
            sg.popup('Authentication error',
                     'Error in Authentication, taking back to main menu.')
            auth = False
            # print('lulu')
            break

        elif (values[0] == settings.get('password', None)):
            sg.popup('Authentication successful',
                     'You can now access the settings menu.')
            auth = True
            # print('aulelele')
            break

    window.close()
    return auth


def change_password(settings):
    layout = [[sg.Text('Enter new password:')], [sg.InputText()], [
        sg.Button('Apply'), sg.Button('Exit')]]
    window = sg.Window('Change Password', layout, finalize=True, modal=True)
    while True:
        event, values = window.read()
        settings.set('password', values[0])
        if event == "Exit" or event == sg.WIN_CLOSED:
            sg.popup('Authentication error',
                     'Error in Authentication, taking back to main menu.')
            break

        elif event == "Apply":
            sg.popup('Password changed successfully')
            break

    window.close()


def main():
    sg.theme('SandyBeach')
    auth = False
    settings = sg.UserSettings(filename='./settings.json')

    window = layout(10, 10)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        elif values[0] == 'Settings Menu':
            if auth == False:
                auth = authenticate(settings)
                if auth == False:
                    window.Element("Main Menu").select()
        if event == 'Change password':
            change_password(settings)
            # print('lalala')
    window.close()


if __name__ == "__main__":
    main()
