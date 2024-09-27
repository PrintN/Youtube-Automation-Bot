import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.exceptions import RefreshError
from lib.config import SCOPES

def refresh_token():
    creds = None
    token_path = 'token.json'
    client_secrets_path = 'client_secrets.json'

    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
            refresh_token = token_data.get('refresh_token')
            token_uri = token_data.get('token_uri')
            client_id = token_data.get('client_id')
            client_secret = token_data.get('client_secret')

        creds = Credentials(
            None, refresh_token=refresh_token, token_uri=token_uri, client_id=client_id, client_secret=client_secret, scopes=SCOPES
        )

    if creds and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
        except RefreshError:
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
    
    return creds

def upload_to_youtube(video_file, metadata, is_short=False):
    creds = refresh_token()

    if creds is None:
        print("Failed to refresh credentials.")
        return

    youtube = build('youtube', 'v3', credentials=creds)

    request_body = {
        'snippet': {
            'title': metadata['title'],
            'description': metadata['description'],
            'tags': metadata['tags'],
            'categoryId': '10',  # Music category
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media
    )

    response = request.execute()
    if is_short:
        print(f"Video uploaded successfully: https://www.youtube.com/shorts/{response['id']}")
    else:
        print(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")
