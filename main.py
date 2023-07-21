import os
import sys
import subprocess
import requests
import PySimpleGUI as sg

KEYCHAIN_SERVICE_NAME = "com.example.app_password"

def set_password(password):
    try:
        subprocess.run(["security", "add-generic-password", "-s", KEYCHAIN_SERVICE_NAME, "-a", "app_user", "-w", password])
        return True
    except subprocess.CalledProcessError:
        return False

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
            sys.exit()
        elif event == "OK":
            expected_password = values["-PASSWORD-"]
            if set_password(expected_password):
                sg.popup("Password set successfully!")
            else:
                sg.popup("Failed to set password.")
            break

    window.close()

def check_additional_password():
    try:
        result = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE_NAME, "-a", "app_user", "-w"], capture_output=True, text=True)
        expected_password = result.stdout.strip()
    except subprocess.CalledProcessError:
        sg.popup("Password not set. Please run the setup again.")
        sys.exit()

    additional_password = sg.popup_get_text("Enter additional password:", password_char="*")

    if additional_password == expected_password:
        sg.popup("Login successful!")
        # Add your code to continue with the login process here
    else:
        sg.popup("Incorrect password. Login failed.")

def self_update():
    url = "https://raw.githubusercontent.com/your_username/your_repo/main/new.py"  # Replace with your GitHub URL
    response = requests.get(url)
    if response.status_code == 200:
        with open(sys.argv[0], "w") as f:
            f.write(response.text)
        sg.popup("App updated successfully. Please restart the app.")
        sys.exit()

def main():
    if not subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE_NAME, "-a", "app_user"], capture_output=True).returncode == 0:
        get_expected_password()

    check_additional_password()

    # Check for updates on GitHub and self-update if needed
    self_update()

if __name__ == "__main__":
    main()
