from flask import Flask, render_template, request
from flask_mail import Mail, Message
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Mail object controls the connection with the host and sends Messages
mail = Mail(app) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    email_address = request.form.get('email')
    content = request.form.get('content')
    try:
        # Message object is essentially the email
        # We are only specifiying the subject of the e-mail, sender, recipient, 
        # and the body. You can also specify html, cc/bcc, attachments, etc.
        message = Message("Trivial Example", sender=os.environ.get('FLASKEMAIL'), recipients=[email_address])
        message.body = content
        mail.send(message)

        return render_template('message.html', title="Trivial - Success", message="E-mail successfully sent.")
    except Exception as e:
        return render_template('message.html', title="Trivial - Exception", message=str(e))