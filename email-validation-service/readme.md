# Email Processing Scripts Documentation

## Overview

This project contains three Python scripts to validate, filter, and send emails. The scripts interact with a MongoDB database, verify email validity, and send notifications.

## Table of Contents

- [emailGrab.py](#emailgrabpy)
- [emailPing.py](#emailpingpy)
- [sendEmail.py](#sendemailpy)
- [Setup & Usage](#setup--usage)
- [Environment Variables](#environment-variables)

---

## `emailGrab.py`

### Description
This script retrieves email addresses from a MongoDB collection, checks their validity, and removes invalid emails from the database.

### Functions
#### `get_collection()`
- Connects to the MongoDB client and returns the `patients` collection.

#### `get_patients()`
- Queries MongoDB for email addresses ending in `@gmail.com`.

#### `filter_emails(invalid_emails: list, patients)`
- Uses multithreading to check if each email is valid.
- Calls `checkEmail` from `emailPing.py`.

#### `delete_patients(invalid_emails: list)`
- Deletes invalid email records from the database.

#### `send_payload(payload: list)`
- Writes invalid emails to a file.
- Encodes the file in base64.
- Sends the file as an attachment via an API.

#### `main()`
- Retrieves patients, filters invalid emails, deletes them, and sends the payload.

---

## `emailPing.py`

### Description
Validates email addresses by checking their structure, MX records, and SMTP responses.

### Function
#### `check_email(email: str)`
- Uses regex to verify the email format.
- Extracts the domain name and checks MX records.
- Attempts to send an SMTP request to verify existence.

---

## `sendEmail.py`

### Description
A Flask-based API that sends email notifications with attachments.

### API Endpoint
#### `POST /process_emails`
- Accepts a JSON payload with email details.
- Calls `send_email(data)` to send the email.

### Function
#### `send_email(data)`
- Constructs an email message.
- Decodes and attaches a file if specified.
- Sends the email via SMTP.

---

## Setup & Usage

### Prerequisites
- Python 3.x
- Required Python packages:
  ```sh
  pip install pymongo dnspython flask
  ```
- A running MongoDB instance.
- A valid SMTP server (Gmail used in this example).

### Running the Scripts

1. Start the email processing server:
   ```sh
   python sendEmail.py
   ```

2. Run the email filtering process:
   ```sh
   python emailGrab.py
   ```

---

## Environment Variables

| Variable            | Description |
|--------------------|-------------|
| `CONNECTION_STRING` | MongoDB connection string |
| `EMAIL_PASSWORD` | Password for the SMTP email sender |

---
