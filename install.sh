import os
import sys
import subprocess
import requests
import PySimpleGUI as sg

KEYCHAIN_SERVICE_NAME = "com.example.app_password"

def set_password(password):
    if sys.platform == "darwin":
        cmd = f'security add-generic-password -s {KEYCHAIN_SERVICE_NAME} -a app_password -w "{password}"'
        subprocess.run(cmd, shell=True)
    else:
        # Add code for storing password on other platforms here
        pass

def get_expected_password():
    if sys.platform == "darwin":
        cmd = f'security find-generic-password -s {KEYCHAIN_SERVICE_NAME} -a app_password -w'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    else:
        # Add code for getting password on other platforms here
        pass

def check_additional_password(expected_password):
    layout = [
        [sg.Text("Please enter the additional password:")],
        [sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("OK")]
    ]

    window = sg.Window("Password Check", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "OK":
            additional_password = values["-PASSWORD-"]
            if additional_password == expected_password:
                sg.popup("Login successful!")
                # Add your code to continue with the login process here
            else:
                sg.popup("Incorrect password. Login failed.")
            break

    window.close()

def self_update():
    # ... (same as before)

def login():
    # ... (same as before)

def main():
    if sys.platform == "darwin":
        if not get_expected_password():
            password = sg.popup_get_text("Set the expected password:", password_char="*")
            set_password(password)

        expected_password = get_expected_password()
        check_additional_password(expected_password)
        # Add your code to proceed after successful login

    else:
        sg.popup("This script only supports macOS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
