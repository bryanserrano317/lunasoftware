import os
import base64
from typing import List
import time
from google_apis import create_service
import configparser



class GmailException(Exception):
	"""gmail base exception class"""

class NoEmailFound(GmailException):
	"""no email found"""

def search_emails(query_string: str, label_ids: List=None):
	try:
		message_list_response = service.users().messages().list(
			userId='me',
			labelIds=label_ids,
			q=query_string
		).execute()

		message_items = message_list_response.get('messages')
		next_page_token = message_list_response.get('nextPageToken')
		
		while next_page_token:
			message_list_response = service.users().messages().list(
				userId='me',
				labelIds=label_ids,
				q=query_string,
				pageToken=next_page_token
			).execute()

			message_items.extend(message_list_response.get('messages'))
			next_page_token = message_list_response.get('nextPageToken')
		return message_items
	except Exception as e:
		raise NoEmailFound('No emails returned')

def get_file_data(message_id, attachment_id, file_name, save_location):
	response = service.users().messages().attachments().get(
		userId='me',
		messageId=message_id,
		id=attachment_id
	).execute()

	file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
	return file_data

def get_message_detail(message_id, msg_format='metadata', metadata_headers: List=None):
	message_detail = service.users().messages().get(
		userId='me',
		id=message_id,
		format=msg_format,
		metadataHeaders=metadata_headers
	).execute()
	return message_detail

if __name__ == '__main__':
	config = configparser.ConfigParser()
	config.read("config.ini")
	CLIENT_FILE = 'client_secret.json'
	API_NAME = 'gmail'
	API_VERSION = 'v1'
	SCOPES = ['https://mail.google.com/']
	service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

	query_string = 'has:attachment'

	save_location = config.get("Directory", "save_path")
	email_messages = search_emails(query_string)

	for email_message in email_messages:
		messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
		messageDetailPayload = messageDetail.get('payload')
		
		if 'parts' in messageDetailPayload:
			for msgPayload in messageDetailPayload['parts']:
				file_name = msgPayload['filename']
				body = msgPayload['body']
				if 'attachmentId' in body:
					attachment_id = body['attachmentId']
					attachment_content = get_file_data(email_message['id'], attachment_id, file_name, save_location)
					
					with open(os.path.join(save_location, file_name), 'wb') as _f:
						_f.write(attachment_content)
						print(f'File {file_name} is saved at {save_location}')
