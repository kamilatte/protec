import subprocess
import PySimpleGUI as sg
import pyotp
import time

KEYCHAIN_SERVICE_NAME = "com.example.app_password"
TWO_FACTOR_SECRET = "your_secret_key"  # Replace this with your own secret key

def set_password(password):
    cmd = f'security add-generic-password -s {KEYCHAIN_SERVICE_NAME} -a app_user -w "{password}"'
    subprocess.run(cmd, shell=True)

def get_expected_password():
    cmd = f'security find-generic-password -s {KEYCHAIN_SERVICE_NAME} -a app_user -w'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def generate_totp_token():
    totp = pyotp.TOTP(TWO_FACTOR_SECRET)
    return totp.now()

def login():
    # Get the expected password from the keychain
    expected_password = get_expected_password()

    layout = [
        [sg.Text("Username:"), sg.Input(key="-USERNAME-")],
        [sg.Text("Password:"), sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Text("Two-Factor Code:"), sg.Input(key="-TOTP-")],
        [sg.Button("Login")]
    ]

    window = sg.Window("Login", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Login":
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]
            totp_code = values["-TOTP-"]

            if password == expected_password:
                # Verify TOTP token
                totp = pyotp.TOTP(TWO_FACTOR_SECRET)
                if totp.verify(totp_code):
                    sg.popup("Login successful!")
                    # Add your code to continue with the login process here
                else:
                    sg.popup("Incorrect TOTP code. Login failed.")
            else:
                sg.popup("Incorrect password. Login failed.")

    window.close()

def main():
    # ... (rest of the code)

if __name__ == "__main__":
    main()
