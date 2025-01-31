from email.message import EmailMessage
import ssl
import smtplib
from flask import Flask, request, jsonify
import os
import base64
import logging

app = Flask(__name__)

@app.route('/process_emails', methods=['POST'])
def process_emails():
    data = request.get_json()
    if not data or "emails" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    send_email(data)
    return jsonify({"status": "Emails processed"}), 200

def send_email(data):
    logging.info("sending email :) ....")

    # Iterate over the cursor to print each document
    try :
        email_sender = os.environ.get("EMAIL_SENDER")
        email_password = os.environ.get("EMAIL_PASSWORD")
        email_receiver = data['receiver']

        subject = data['subject']
        body = data['body']

        file_name = data['file_name']
        file_data = data['file_data']
            
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)


        if data['attachment']:
            binary_data = base64.b64decode((file_data).encode('utf-8'))

            directory = os.path.dirname(file_name)
            if directory:  # Only create directories if a path is specified
                os.makedirs(directory, exist_ok=True)

            with open(file_name, "wb") as f:
                f.write(binary_data)

            with open(file_name, "rb") as f:
                file_data = f.read()
                em.add_attachment(file_data,
                                  maintype='text',
                                  subtype='plain',
                                  filename=os.path.basename(file_name))

        context = ssl.create_default_context()

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
        logging.info("email sent: " + email_receiver)
    except Exception as e:
        logging.error(repr(e))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)