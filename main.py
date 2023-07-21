import os
import sys
import subprocess
import requests
import PySimpleGUI as sg

KEYCHAIN_SERVICE_NAME = "com.example.app_password"
MAX_LOGIN_ATTEMPTS = 3  # Maximum number of login attempts allowed
UPDATE_URL = "https://raw.githubusercontent.com/alwayshyper/protec/main/new.py"  # Replace with your GitHub URL

def set_password(password):
    # ... (same as before)

def get_expected_password():
    # ... (same as before)

def check_additional_password():
    # ... (same as before)

def self_update():
    # ... (same as before)

def login():
    # ... (same as before)

def main():
    if not subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE_NAME, "-a", "app_user"], capture_output=True, text=True).stdout.strip():
        get_expected_password()

    login_successful = False
    attempts = 0

    while not login_successful and attempts < MAX_LOGIN_ATTEMPTS:
        login_successful = check_additional_password()
        attempts += 1

    if login_successful:
        # Check for updates and self-update (same as before)
        # ...
    else:
        sg.popup("Incorrect password. Login failed.")
        sys.exit()

if __name__ == "__main__":
    main()
