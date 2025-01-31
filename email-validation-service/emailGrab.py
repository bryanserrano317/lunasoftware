from pymongo import MongoClient
from emailPing import checkEmail
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os
import base64
import logging
import configparser


def get_collection():
# Connect to the MongoDB client
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
    if not CONNECTION_STRING:
        raise EnvironmentError("CONNECTION_STRING is not set in the environment variables.")
    client = MongoClient(CONNECTION_STRING, 27017)  # Replace with your MongoDB connection string

    # Select the database and collection
    db = client.get_database(config["DATABASE"]["name"])
    test_collection = db.get_collection(config["DATABASE"]["collection"])

    return test_collection

def get_patients():
    test_collection = get_collection()
    # Query to find entries where the email does NOT contain '@'
    query = {"email": {"$regex": "@gmail\\.com$"}}

    # Fetch matching entries
    patients = test_collection.find(query)

    patients = list(patients)

    return patients

def filter_emails(invalid_emails: list, patients):
    total = len(patients)
    if total == 0:
        logging.info("No emails to check.")
        return invalid_emails

    # Use ThreadPoolExecutor to run checkEmail calls in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each checkEmail task and store the future -> patient mapping
        futures = {executor.submit(checkEmail, p['email']): p for p in patients}

        # Process results as they are completed
        for i, future in enumerate(as_completed(futures), start=1):
            patient = futures[future]
            try:
                is_valid = future.result()  # Get the result of checkEmail
                if not is_valid:
                    invalid_emails.append(patient)
            except Exception as e:
                # Handle exceptions from checkEmail if necessary
                logging.info(f"Error checking {patient['email']}: {e}")

            # logging.info progress at intervals or on the last iteration
            if i % 3 == 0 or i == total:
                percentage = (i / total) * 100
                logging.info(f"Checked {i}/{total} emails ({percentage:.2f}%)...", end='\r', flush=True)

    # logging.info a final summary after all checks are done
    logging.info(f"\nFinished checking {total} emails. Found {len(invalid_emails)} invalid emails.")
    return invalid_emails

def delete_patients(invalid_emails: list):
    test_collection = get_collection()
    try:
        ids = [patient['_id'] for patient in invalid_emails]
        result = test_collection.delete_many({"_id": {"$in": ids}})
    except Exception as e:
        logging.info('An Error Occured', e)
        return False
    logging.info("Finished")
    return True

def send_payload(payload: list):
    with open(config["OUTPUT_FILE"]["name"], "w") as f:
        f.write("\n".join(emails))

    with open(config["OUTPUT_FILE"]["name"], "rb") as f:
        file_data = f.read()

    encoded_data = base64.b64encode(file_data).decode('utf-8')

    url = config["EMAIL_API"]["URL"]
    headers = {'Content-Type': 'application/json'}
    payload = {"emails": emails, 
            "receiver": config["EMAIL"]["receiver"], 
            "subject": "Invalid Emails",
            "body": "Attached is a file containing all invalid 'gmail' address found.",
            "attachment": True, 
            "file_data": encoded_data,
            "file_name": "invalid-emails.txt"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        logging.info("Payload sent successfully and is being processed.")
        logging.info("Server Response:", response.json())
    else:
        logging.error("Failed to send payload:", response.text)

def main():
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("config.ini")

    patients = get_patients()
    invalid_emails = filter_emails([], patients)

    logging.info(delete_patients(invalid_emails))

    payload = [patient['email'] for patient in invalid_emails]

    send_payload(payload)


if __name__ == "__main__":
    main()
