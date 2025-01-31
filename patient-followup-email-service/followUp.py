from datetime import datetime
import time

import os
import string
import ssl
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

CONNECTION_STRING = os.environ.get("CONNECTION_STRING")


def sendEmail(collection):
    print("sending email :) ....")

    patients = test_collection.find({"followUp": False})

    # Iterate over the cursor to print each document
    for patient in patients:
        test_collection.update_one({"_id": patient['_id']}, {"$set": {"followUp": True}})       
        try :
            time.sleep(6)
            email_sender = os.environ.get("EMAIL_SENDER")
            email_password = os.environ.get("EMAIL_PASSWORD")
            email_receiver = patient['email']

            subject = config.get('Email', 'subject') + (patient['firstName']).title()
            body = "Hi " + (patient['firstName']).title() + ", " + config.get('Email', 'body')


                
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            print("email sent: " + email_receiver)
        except Exception as e:
            print(repr(e))
            continue
            
try:
    client = MongoClient(CONNECTION_STRING, 27017)

    db = client.get_database(config.get('Database', 'name'))

    test_collection = db.get_collection(config.get('Database', 'collection'))

except Exception as e:
    print(repr(e), "error occured")
    pass  
sendEmail(test_collection)

