import serial
import time
import re
from twilio.rest import Client

# === Twilio Config ===
account_sid = 'AC1e27df30fb90cccb4a40c214af553689'
auth_token = '851582cfbaf7c6cf28374278ec294d9d'
twilio_sms_number = '+19104000152'
your_sms_number = '+919711234945'

client = Client(account_sid, auth_token)

# === Serial Config ===
try:
    ser = serial.Serial('COM3', 9600)
    time.sleep(2)
    print("Serial connection established on COM3.")
except serial.SerialException as e:
    print(f"[ERROR] Could not open serial port: {e}")
    exit(1)

notified = False
threshold = 100

print("Listening for gas detection...")

while True:
    try:
        raw_data = ser.readline().decode().strip()
        print(f"Received from sensor: '{raw_data}'")

        # Extract number using regex
        match = re.search(r'\d+', raw_data)
        if match:
            value = int(match.group())
            print(f"Parsed sensor value: {value}")

            if value > threshold and not notified:
                print(f"[ALERT] Value {value} exceeds threshold {threshold}. Sending SMS...")

                try:
                    message = client.messages.create(
                        body="🚨 Gas leakage detected! Buzzer triggered!",
                        from_=twilio_sms_number,
                        to=your_sms_number
                    )
                    print(f"[SUCCESS] SMS sent. SID: {message.sid}")
                    notified = True
                    time.sleep(60)
                    notified = False

                except Exception as sms_error:
                    print(f"[ERROR] Failed to send SMS: {sms_error}")
        else:
            print("[INFO] No numeric value found in data. Ignoring.")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
