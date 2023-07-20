import PySimpleGUI as sg

def get_expected_password():
    layout = [
        [sg.Text("Please enter the expected password:")],
        [sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("OK")]
    ]

    window = sg.Window("Password Setup", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "OK":
            expected_password = values["-PASSWORD-"]
            with open("expected_password.txt", "w") as password_file:
                password_file.write(expected_password)
            break

    window.close()

def check_additional_password():
    with open("expected_password.txt", "r") as password_file:
        expected_password = password_file.readline().strip()

    additional_password = sg.popup_get_text("Enter additional password:", password_char="*")

    if additional_password == expected_password:
        sg.popup("Login successful!")
        # Add your code to continue with the application functionality here
    else:
        sg.popup("Incorrect password. Login failed.")

def main():
    if not os.path.exists("expected_password.txt"):
        get_expected_password()

    check_additional_password()

if __name__ == "__main__":
    main()
