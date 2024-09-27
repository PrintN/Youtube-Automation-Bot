import requests
import json
import os
from lib.config import PIXABAY_API_KEY, FREESOUND_API_KEY, USED_CONTENT_FILE
from lib.utils import download_file

def load_used_content():
    if os.path.exists(USED_CONTENT_FILE):
        with open(USED_CONTENT_FILE, 'r') as file:
            return json.load(file)
    return {'videos': [], 'audios': []}

def save_used_content(content):
    with open(USED_CONTENT_FILE, 'w') as file:
        json.dump(content, file, indent=4)

def search_and_download_meditation_video(used_videos, video_query):
    search_url = "https://pixabay.com/api/videos/"
    params = {'key': PIXABAY_API_KEY, 'q': video_query}
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        data = response.json()
        for hit in data['hits']:
            video_url = hit['videos']['medium']['url']
            if video_url not in used_videos:
                print(f"Video found: {video_url}")
                download_file(video_url, "video.mp4")
                return video_url
        print("No new videos found.")
    else:
        print(f"Error: {response.status_code}")
    return None

def search_and_download_music(query, used_audios):
    search_url = f"https://freesound.org/apiv2/search/text/?query={query}&sort=rating_desc&token={FREESOUND_API_KEY}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        for result in data['results']:
            sound_id = result['id']
            details_url = f"https://freesound.org/apiv2/sounds/{sound_id}/?token={FREESOUND_API_KEY}"
            sound_details = requests.get(details_url).json()
            
            if "previews" in sound_details:
                audio_url = sound_details['previews'].get('preview-hq-mp3') or sound_details['previews'].get('preview-hq-wav')
                if audio_url and audio_url not in used_audios:
                    download_file(audio_url, "music.mp3")
                    return audio_url, sound_details.get('license', '')

    print("No new music found.")
    return None, None
