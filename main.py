import io
import pyotp
import qrcode
from PIL import Image
import PySimpleGUI as sg

def generate_otp_secret():
    # Generate a random OTP secret
    return pyotp.random_base32()

def generate_otp_uri(account_name, otp_secret):
    return f'otpauth://totp/{account_name}?secret={otp_secret}&issuer=MyApp'

def confirm_otp(otp_secret):
    layout = [
        [sg.Text("Enter the One-Time Password (OTP):"), sg.Input(key='-OTP_INPUT-')],
        [sg.Button("Confirm"), sg.Button("Cancel")],
    ]

    window = sg.Window("Confirm OTP", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            window.close()
            return False
        elif event == "Confirm":
            otp_input = values['-OTP_INPUT-']
            totp = pyotp.TOTP(otp_secret)
            if totp.verify(otp_input):
                window.close()
                return True
            else:
                sg.popup("Incorrect OTP. Please try again.", title="Invalid OTP")

def setup_2fa():
    # Create a simple GUI to set up 2FA
    layout = [
        [sg.Text("Account Name:"), sg.Input(key='-ACCOUNT_NAME-')],
        [sg.Button("Generate OTP Secret"), sg.Button("Generate QR Code"), sg.Button("Exit")],
        [sg.Image(key='-IMAGE-')],
    ]

    window = sg.Window("2FA Setup", layout)

    otp_secret = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Generate OTP Secret":
            otp_secret = generate_otp_secret()
            sg.popup(f"Generated OTP Secret:\n{otp_secret}", title="OTP Secret")
        elif event == "Generate QR Code" and otp_secret:
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

            byte_stream = show_qr_code(qr)
            window['-IMAGE-'].update(data=byte_stream.getvalue())

        elif event == "Confirm" and otp_secret:
            if confirm_otp(otp_secret):
                sg.popup("2FA Setup Completed Successfully!", title="Success")
            else:
                sg.popup("2FA Setup Canceled.", title="Canceled")

    window.close()

def show_qr_code(qr):
    img = qr.make_image(fill_color="black", back_color="white")
    byte_stream = io.BytesIO()
    img.save(byte_stream, format='PNG')
    byte_stream.seek(0)
    return byte_stream

def main():
    setup_2fa()

if __name__ == "__main__":
    main()
