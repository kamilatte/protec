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
    # Create a modern theme for the GUI
    sg.theme('Dark Blue 3')

    # Create a simple GUI to set up 2FA
    layout = [
        [sg.Text("Account Name:"), sg.Input(key='-ACCOUNT_NAME-')],
        [sg.Button("Show OTP Secret"), sg.Button("Next"), sg.Button("Exit")],
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
        elif event == "Next":
            account_name = values['-ACCOUNT_NAME-']
            otp_uri = generate_otp_uri(account_name, otp_secret)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(otp_uri)
            qr.make(fit=True)

            byte_stream = show_qr_code(otp_secret)
            window['-IMAGE-'].update(data=byte_stream.getvalue())

            # Auto-focus the first input field
            window['-OTP-1-'].SetFocus()

            # Enable event handling to move focus to the next input field
            for i in range(1, 7):
                window['-OTP-{}-'.format(i)].expand(expand_x=True, expand_y=True)
                window['-OTP-{}-'.format(i)].bind("<Tab>", f"{i + 1}.1")
                window['-OTP-{}-'.format(i)].bind("<BackSpace>", f"{i - 1}.1")
            window['-OTP-6-'].bind("<Tab>", "1.1")
            window['-OTP-1-'].bind("<BackSpace>", "6.1")

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
    # Add the code for confirming OTP here
    pass

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
