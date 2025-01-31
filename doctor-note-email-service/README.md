# Project Documentation

## Overview
This project consists of multiple Python scripts that handle email parsing, file extraction, and Google API interactions. Below is a breakdown of each script and its functionalities.

---

## `email_parser.py`
This script processes RTF files, extracts text, and sends emails using SMTP. It also interacts with a MongoDB database and handles file operations.

### Dependencies
- `striprtf`
- `openpyxl`
- `smtplib`
- `pymongo`
- `pandas`

### Key Functions
- `readFiles(config, num, fileName, outputFile, file_path, path)`: Reads RTF files and extracts text.
- `send_email(subject, body, recipient)`: Sends emails using `smtplib`.
- `connect_to_mongo(uri, db_name)`: Establishes a connection to MongoDB.

---

## `extractor.py`
This script scans a directory for ZIP files, extracts them, and moves the extracted contents to a destination directory.

### Dependencies
- `os`
- `shutil`
- `zipfile`

### Key Functions
- `process_all_zip_files(directory_path, destination_dir)`: Extracts ZIP files and deletes them after extraction.

---

## `Google.py`
This script interacts with Gmail using Google APIs. It allows searching emails based on specific queries.

### Dependencies
- `google_apis.py`
- `base64`
- `google-auth`
- `googleapiclient.discovery`

### Key Functions
- `search_emails(query_string, label_ids)`: Searches for emails in Gmail based on query parameters.
- `GmailException`: Base class for Gmail-related exceptions.

---

## `google_apis.py`
This script handles Google API authentication and service creation.

### Dependencies
- `google_auth_oauthlib.flow`
- `google.oauth2.credentials`
- `google.auth.transport.requests`

### Key Functions
- `create_service(client_secret_file, api_name, api_version, *scopes)`: Authenticates and initializes a Google API service.

---

## Usage
1. Ensure that all dependencies are installed (`pip install -r requirements.txt`).
2. Configure the necessary API credentials for Google services.
3. Run individual scripts as needed for email parsing, file extraction, or Google API operations.

---

## License
This project is licensed under [Your License Here].
