from flask import Flask, send_file, redirect
import qrcode

app = Flask(__name__)

def get_last_number():
    try:
        with open('numbers.txt', 'r') as file:
            last_number = int(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, start with 0
        last_number = 0
    return last_number

def save_new_number(number):
    with open('numbers.txt', 'w') as file:
        file.write(str(number))
@app.route('/')
def index():
    return redirect('/get_qr_code')

@app.route('/get_qr_code')
def get_qr_code():
    # Get the last saved number
    last_number = get_last_number()

    # Generate the next number
    next_number = last_number + 1

    # Create a QR code with the next number
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(f"https://large-type.com/#*{next_number}*")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code image to a file
    img.save(f'qr_code_{next_number}.png')

    # Save the new number to the file
    save_new_number(next_number)

    # Send the QR code image to the client
    return send_file(f'qr_code_{next_number}.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
