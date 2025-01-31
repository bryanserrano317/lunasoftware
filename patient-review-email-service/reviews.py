from datetime import datetime
import time

import os
import string
import ssl
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
import configparser

CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
config = configparser.ConfigParser()
config.read("config.ini")



def sendEmail(collection):
    print("sending email :) ....")

    patients = test_collection.find({"review": False})

    # Iterate over the cursor to print each document
    for patient in patients:
        test_collection.update_one({"_id": patient['_id']}, {"$set": {"review": True}})       
        try :
            time.sleep(50)
            email_sender = os.environ.get("EMAIL_SENDER")
            email_password = os.environ.get("EMAIL_PASSWORD")
            email_receiver = patient['email']

            subject = config.get("Email", "subject") + (patient['firstName']).title() +  ' !'
            body = "Dear " + (patient['firstName']).title() + ", " + 


                
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
    print("starting..")
    client = MongoClient(CONNECTION_STRING, 27017)

    db = client.get_database(config.get("Database", "name"))

    test_collection = db.get_collection(config.get("Database", "collection"))

except Exception as e:
    print(repr(e), "error occured")
    pass  
sendEmail(test_collection)

