PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
PIN = None
recipients = ['0043xxxxxxxxxx']

from gsmmodem.modem import GsmModem
from flask import Flask, request

modem = GsmModem(PORT, BAUDRATE)
modem.connect(PIN)
app = Flask(__name__)

@app.route('/send', methods=['GET'])
def send():
    try:
        msg = request.args.get('msg')
        for recipient in recipients:
            modem.sendSms(recipient, msg, waitForDeliveryReport=True)
        return 'success'
    except:
        return 'error'

app.run(port=3000)
