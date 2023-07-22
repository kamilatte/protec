import os
import sys
import subprocess
import requests
import PySimpleGUI as sg
import qrcode
import pyotp

KEYCHAIN_SERVICE_NAME = "com.example.app_password"

def set_2fa_key(key):
    if sys.platform == "darwin":
        cmd = f'security add-generic-password -s {KEYCHAIN_SERVICE_NAME} -a 2fa_key -w "{key}"'
        subprocess.run(cmd, shell=True)

def get_2fa_key():
    if sys.platform == "darwin":
        cmd = f'security find-generic-password -s {KEYCHAIN_SERVICE_NAME} -a 2fa_key -w'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

def create_2fa_key():
    return pyotp.random_base32()

def generate_qr_code(key):
    totp = pyotp.TOTP(key)
    url = totp.provisioning_uri(name="Example User", issuer_name="Example App")
    qr = qrcode.make(url)
    return qr

def show_qr_code(qr):
    layout = [
        [sg.Text("Scan the QR code with your 2FA app:")],
        [sg.Image(data=qr.tobytes())],
        [sg.Button("OK")]
    ]

    window = sg.Window("2FA Setup", layout, finalize=True)

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            window.close()
            break

def setup_2fa():
    key = create_2fa_key()
    set_2fa_key(key)
    qr_code = generate_qr_code(key)
    show_qr_code(qr_code)

def login():
    sg.theme("DarkGrey3")
    layout = [
        [sg.Text("Enter 6-digit 2FA code:")],
        [sg.Input(key="-2FA-", size=(10, 1))],
        [sg.Button("Login")]
    ]

    window = sg.Window("2FA Login", layout, finalize=True)
    window.Maximize()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            sys.exit(0)
        elif event == "Login":
            expected_key = get_2fa_key()
            user_input = values["-2FA-"]
            totp = pyotp.TOTP(expected_key)
            if totp.verify(user_input):
                window.close()
                return True
            else:
                sg.popup("Invalid 2FA code. Please try again.")

def main():
    sg.popup("Welcome! Click OK to set up 2FA.")
    setup_2fa()
    if login():
        sg.popup("2FA Login successful!")
        # Add your code to proceed after successful login

if __name__ == "__main__":
    main()
