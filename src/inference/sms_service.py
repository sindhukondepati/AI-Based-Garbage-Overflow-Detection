import os
from twilio.rest import Client

def send_sms(message):
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE")
    to_phone = os.getenv("MUNICIPALITY_PHONE")

    # fallback protection
    if not all([sid, token, from_phone, to_phone]):
        print("⚠️ Twilio not configured. MOCK SMS SENT")
        print(message)
        return {"status": "mock"}

    try:
        client = Client(sid, token)
        msg = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        return {"status": "sent", "sid": msg.sid}
    except Exception as e:
        print("❌ SMS failed:", e)
        return {"status": "failed"}
