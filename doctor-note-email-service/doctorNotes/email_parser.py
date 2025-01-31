from striprtf.striprtf import rtf_to_text
import os
import openpyxl
import string
import datetime
import ssl
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import traceback
import time
from pymongo import MongoClient
import pandas as pd
import configparser

def readFiles(config, num, fileName, outputFile, file_path, path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text = rtf_to_text(content)

        res = list(text)

        i = 0
        j = i + 1

        while res[j] != "#":
            j += 1
        res[i : j + 1] = ""
        j = i + 1

        patientNumber = ''.join(res[i:i + 6])

        patientName = ""

        for k in range(i, 100):
            if ''.join(res[i:j]) == config.get('EmailContent', 'initial_greeting'):
                i,j = j, j + 1
                while res[j] != ',':
                    patientName += res[j]
                    j += 1
                break
            elif len(''.join(res[i:j + 1])) == 10:
                i += 1
                j = i + 1
            j += 1
        i = i + len(patientName)

        patientName = patientName.split(' ', 1)[0]
        os.chdir(path)
        logWrite(num, patient_name, patient_number, file_name, 
                 res, outputFile)
        sendEmail(config, patientNumber, res, file_path, patientName)
    except Exception:
        traceback.print_exc()
        pass

def sendEmail(config, patientNumber, res, file_path, patientName):
    patient =  test_collection.find_one({"id": patientNumber})  
    if (patient):

               
        res[0 : 7] = ""
        abc = ''.join(res)
       
        os.remove(file_path)

        
        email_sender = config.get('Email', 'sender')
        email_password = config.get('Email', 'password')
        email_receiver = config.get('Email', 'sender')
        
        subject_template = config.get('Email', 'subject_template')
        patient_name = patient['firstName'].title()
        subject = subject_template.format(patient_name=patient_name)
        body = str(abc) +  config.get('EmailContent', 'additional_footer')
        em = EmailMessage()
        em = MIMEText(body)
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.add_header('Content-Type', 'text')
        
        
        context = ssl.create_default_context()
        print("sending email.....")
        with smtplib.SMTP(config.get('Email', 'smtp_server'), 
                          int(config.get('Email', 'smtp_port'))) as smtp:
           smtp.ehlo()
           smtp.starttls()
           smtp.ehlo()
           smtp.login(email_sender, email_password)
           smtp.sendmail(email_sender, email_receiver, em.as_string())
           print("email sent: ",  email_receiver)

        time.sleep(config.get('Sleep', 'time_between_emails'))
        
        return [fileName, int(patientNumber), patientName]
              
    

def logWrite(num, patient_name, patient_number, file_name, body, 
             outputFile):
    outputFile.write(("---------------" + "\n"))
    outputFile.write((str(num) + "\n"))
    outputFile.write(("---------------" + "\n"))
    outputFile.write((str(patientName) + "\n"))
    outputFile.write(("---------------" + "\n"))
    outputFile.write((str(patientNumber) + "\n"))
    outputFile.write(("---------------" + "\n"))
    outputFile.write((str(fileName) + '\n'))
    outputFile.write(("---------------" + "\n"))
    outputFile.write((str(patientName) + config.get('Email', 'subject')))
    outputFile.write(("---------------" + "\n"))
    outputFile.write((''.join(body))) 

def add_to_database(config):
    for file in os.listdir():
       if file.endswith(".csv"):
           file_name = file
           read_file = pd.read_csv(file_name)
           read_file.to_excel(config.get('Misc', 'xlsx_log_filename'), 
                              index=None, header=True)
           file_name = config.get('Misc', 'xlsx_log_filename')

    wb2 = openpyxl.load_workbook(file_name)
    ws2 = wb2.active
    
    patient_collection = connect_to_database(config)
    print("Reading Excel File...")
    for row in ws2.iter_rows(values_only=True):
        data = { 
                "firstName": row[0], 
                "lastName": row[1], 
                "email": row[2],
                "id": row[3], 
                "review": True, 
                "followUp": True
        }
        existingUser = patient_collection.find_one({"id": row[3]})
        if not existingUser and data["email"] != "No Email":
            print("Adding: ", data["email"])
            patient_collection.insert_one(data)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    path = config.get('Paths', 'logs_path')
    path2 = config.get('Paths', 'downloads_path')
    os.chdir(path2)
    
    add_to_database(config)

    allData = []
    num = 0

    os.chdir(path)

    if os.path.exists(config.get('Misc', 'email_log_filename')):
      os.remove(config.get('Misc', 'email_log_filename'))
    else:
      createFile = open(config.get('Misc', 'email_log_filename'), "x")

    outputFile = open(config.get('Misc', 'email_log_filename'), "a")

    os.chdir(path2)

    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".rtf"):
            print(file)
            file_path = f"{path2}/{file}"
            num += 1
      
            allData.append(readFiles(config, num, file, outputFile, 
                                     file_path, path))



def connect_to_database(config):
    CONNECTION_STRING = config.get('Database', 'connection_string')
    try:
        client = MongoClient(CONNECTION_STRING, int(config.get('Database', 'database_port')))

        db = client.get_database(config.get('Database', 'database_name'))

        patient_collection = db.get_collection(config.get('Database', 'collection_name'))
        return patient_collection

    except Exception as e:
        print("An error occurred:", e)
    
if __name__ == "__main__":
    main()

