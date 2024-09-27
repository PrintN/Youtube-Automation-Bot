import os
import json
from dotenv import load_dotenv

load_dotenv()

PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY')
FREESOUND_API_KEY = os.environ.get('FREESOUND_API_KEY')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
USED_CONTENT_FILE = 'used_content.json'

def load_config():
    with open('auto.json', 'r') as f:
        return json.load(f)
