import PySimpleGUI as sg

EXPECTED_PASSWORD_FILE = "/Users/always_haker/.myscript/expected_password.txt"

def get_expected_password():
    layout = [
        [sg.Text("Please enter the expected password:")],
        [sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("OK")]
    ]

    window = sg.Window("Password Setup", layout, finalize=True, no_titlebar=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "OK":
            expected_password = values["-PASSWORD-"]
            with open(EXPECTED_PASSWORD_FILE, "w") as password_file:
                password_file.write(expected_password)
            break

    window.close()

def check_additional_password():
    with open(EXPECTED_PASSWORD_FILE, "r") as password_file:
        expected_password = password_file.readline().strip()

    layout = [
        [sg.Text("Enter additional password:")],
        [sg.Input(key="-ADDITIONAL-PASSWORD-", password_char="*")],
        [sg.Button("OK")]
    ]

    window = sg.Window("Login", layout, finalize=True, no_titlebar=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "OK":
            additional_password = values["-ADDITIONAL-PASSWORD-"]
            if additional_password == expected_password:
                sg.popup("Login successful!")
                # Add your code to continue with the login process here
            else:
                sg.popup("Incorrect password. Login failed.")
            break

    window.close()

def main():
    get_expected_password()
    check_additional_password()

if __name__ == "__main__":
    main()
