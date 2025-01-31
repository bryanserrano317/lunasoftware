# Reviews Script Documentation

## Overview
`reviews.py` is a Python script designed to send review-related email notifications using `smtplib` and interact with a MongoDB database. It retrieves configuration settings from a `config.ini` file and uses environment variables for secure database connections.

---

## Dependencies
- `datetime` - For handling date and time operations.
- `smtplib` - For sending emails.
- `email.message` - To construct email messages.
- `pymongo` - For MongoDB interactions.
- `configparser` - For reading configuration files.
- `os` - For accessing environment variables.

---

## Key Functions

### `sendEmail(collection)`
- Prints a message indicating that an email is being sent.
- Likely retrieves data from the MongoDB collection and sends emails related to reviews.

### Configuration and Environment Variables
- Reads configurations from `config.ini`.
- Uses `CONNECTION_STRING` from environment variables to connect to MongoDB.

---

## Usage
1. Ensure all dependencies are installed: `pip install pymongo`.
2. Set up `config.ini` with necessary configurations.
3. Export `CONNECTION_STRING` as an environment variable.
4. Run the script: `python reviews.py`.

---

## License
This project is licensed under [Your License Here].
