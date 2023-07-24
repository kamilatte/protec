import io
import pyotp
import qrcode
from PIL import Image
import PySimpleGUI as sg
import os
import keyring

APP_NAME = "MyApp"

def generate_otp_secret():
    # Generate a random OTP secret
    return pyotp.random_base32()

def generate_otp_uri(account_name, otp_secret):
    return f'otpauth://totp/{account_name}?secret={otp_secret}&issuer={APP_NAME}'

def setup_2fa():
    # Create a simple GUI to set up 2FA
    layout = [
        [sg.Text("Account Name:"), sg.Input(key='-ACCOUNT_NAME-')],
        [sg.Button("Show OTP Secret"), sg.Button("Exit")],
        [sg.Image(key='-IMAGE-')],
    ]

    window = sg.Window("2FA Setup", layout, finalize=True)

    otp_secret = generate_otp_secret()
    qr_byte_stream = show_qr_code(otp_secret)
    window['-IMAGE-'].update(data=qr_byte_stream.getvalue())

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Show OTP Secret":
            sg.popup(f"Generated OTP Secret:\n{otp_secret}", title="OTP Secret")

    window.close()
    save_otp_secret(otp_secret)

def show_qr_code(otp_secret):
    otp_uri = generate_otp_uri("MyAccount", otp_secret)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    byte_stream = io.BytesIO()
    img.save(byte_stream, format='PNG')
    byte_stream.seek(0)
    return byte_stream

def confirm_otp(otp_secret):
    # Create a simple GUI for 2FA confirmation
    layout = [
        [sg.Text("Enter 6-Digit Verification Code:")],
        [sg.Input(size=(1, 1), key='-OTP-1-', justification='center', enable_events=True),
         sg.Input(size=(1, 1), key='-OTP-2-', justification='center', enable_events=True),
         sg.Input(size=(1, 1), key='-OTP-3-', justification='center', enable_events=True),
         sg.Input(size=(1, 1), key='-OTP-4-', justification='center', enable_events=True),
         sg.Input(size=(1, 1), key='-OTP-5-', justification='center', enable_events=True),
         sg.Input(size=(1, 1), key='-OTP-6-', justification='center', enable_events=True),
         ],
        [sg.Button("Verify"), sg.Button("Resend OTP"), sg.Button("Exit")],
    ]

    window = sg.Window("2FA Verification", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            window.close()
            break
        elif event == "Resend OTP":
            # Code to resend the OTP (you can implement this function)
            # For demonstration purposes, we'll simply print a message
            print("OTP Resent")
        elif event == "Verify":
            otp_digits = [values[f'-OTP-{i}-'] for i in range(1, 7)]
            otp_code = "".join(otp_digits)

            # Verify the OTP code (you can implement this function)
            # For demonstration purposes, we'll simply print the code
            print("OTP Code:", otp_code)

    window.close()

    # Create a simple GUI to prompt for the OTP
    layout = [
        [sg.Text("Enter One-Time Password:"), sg.Input(key='-OTP-')],
        [sg.Button("Verify OTP"), sg.Button("Exit")],
    ]

    window = sg.Window("2FA Verification", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Verify OTP":
            entered_otp = values['-OTP-']
            totp = pyotp.TOTP(otp_secret)
            if totp.verify(entered_otp):
                sg.popup("OTP Verification Successful!", title="Success")
                window.close()
                break
            else:
                sg.popup("Invalid OTP! Please try again.", title="Error")

    window.close()

def save_otp_secret(otp_secret):
    # Use keyring to securely store the OTP secret
    keyring.set_password(APP_NAME, "otp_secret", otp_secret)

def load_otp_secret():
    # Load the OTP secret from the keyring
    return keyring.get_password(APP_NAME, "otp_secret")

def main():
    # Check if the 2FA setup is completed or not
    if not load_otp_secret():
        # OTP secret is not found, set up 2FA
        setup_2fa()
    else:
        # 2FA setup is completed, prompt for 2FA code
        otp_secret = load_otp_secret()
        confirm_otp(otp_secret)

if __name__ == "__main__":
    main()
