from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender=request.form.get('From')
    num_media = request.values.get("NumMedia")
    if num_media=='0':
        resp = MessagingResponse()
        msg_rep = fetch_reply(msg, sender)
        if len(msg_rep[1]) > 0:
            resp.message(msg_rep[0]).media(msg_rep[1])
        else:
            resp.message(msg_rep[0])

        return str(resp)
    else:
        resp=MessagingResponse()
        resp.message('''Thanks for sending me media
but i can't recognise it now
i need some feature upgradation
        ''')
        return str(resp)

    # Create reply


if __name__ == "__main__":
    app.run(debug=True)