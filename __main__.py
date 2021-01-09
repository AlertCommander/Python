recipients = ['+436503552474']
tokens = ['abc123']
device = "/dev/ttyUSB0"
escalation_levels = ["Emergency", "Alert", "Critical", "Error", "Warning", "Notice", "Informational", "Debug"]

import serial
import time

from flask import Flask, request
app = Flask(__name__)

modem = serial.Serial(device,  9600, timeout=5)

def send_sms(recipient, message):
    time.sleep(0.5)
    modem.write(b'ATZ\r')
    time.sleep(0.5)
    modem.write(b'AT+CMGF=1\r')
    time.sleep(0.5)
    modem.write(b'AT+CMGS="' + recipient.encode() + b'"\r')
    time.sleep(0.5)
    modem.write(message.encode() + b"\r")
    time.sleep(0.5)
    modem.write(bytes([26]))
    time.sleep(0.5)


@app.route('/send', methods=['GET'])
def send():
    try:
        msg = request.args.get('msg')
        token = request.args.get('token')
        level = request.args.get('level')

        escalation_msg = escalation_levels[level]
        msg = escalation_msg + "! \n" + msg

        if token not in tokens:
            return 'unauthorized'
        for recipient in recipients:
            send_sms(recipient, msg)
        return 'success'
    except:
        return 'error'

app.run(host='0.0.0.0', port=3000)