import requests
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx.all import audio_loop
import os
import sys
import json
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.exceptions import RefreshError

load_dotenv()

PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY')
FREESOUND_API_KEY = os.environ.get('FREESOUND_API_KEY')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
USED_CONTENT_FILE = 'used_content.json'


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
    
    params = {
        'key': PIXABAY_API_KEY,
        'q': video_query
    }
    
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

            license_type = sound_details.get('license', '')
            if license_type == "https://creativecommons.org/licenses/by/4.0/":
                title = sound_details.get('name', 'Unknown Title')
                author = sound_details.get('username', 'Unknown Author')
                sound_url = f"https://freesound.org/s/{sound_id}/"
                attribution_text = f"{title} by {author} -- {sound_url} -- License: Attribution 4.0"
                
                if 'previews' in sound_details:
                    if 'preview-hq-mp3' in sound_details['previews']:
                        audio_url = sound_details['previews']['preview-hq-mp3']
                        file_format = ".mp3"
                    elif 'preview-hq-wav' in sound_details['previews']:
                        audio_url = sound_details['previews']['preview-hq-wav']
                        file_format = ".wav"
                    else:
                        print("No suitable audio format found.")
                        return None, None
                    
                    if audio_url not in used_audios:
                        print(f"Music found: {audio_url}")
                        print(f"Attribution: {attribution_text}")
                        download_file(audio_url, f"music{file_format}")

                        return audio_url, attribution_text

        print("No new music found.")
    else:
        print(f"Error: {response.status_code}")
    return None, None

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded: {filename}")


def combine_audio_video(video_file, audio_file, output_file, duration_minutes=60):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    duration_seconds = duration_minutes * 60

    video_loop = concatenate_videoclips([video] * (duration_seconds // int(video.duration) + 1)).subclip(0, duration_seconds)
    audio_looped = audio_loop(audio, duration=duration_seconds)

    final_video = video_loop.set_audio(audio_looped)

    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

    video.close()
    audio.close()
    final_video.close()


def generate_metadata(query, duration_minutes, attribution=None):
    title = f"Relaxing {query.capitalize()} Music ({duration_minutes} minutes)"
    description = f"This is a {duration_minutes}-minute {query} video with soothing music to help you relax and meditate."
    
    if attribution:
        description += f"\n\n🎶Music attribution🎶\n{attribution}"

    tags = [query, "relaxation", "calm", "soothing music", "meditation"]

    metadata = {
        'title': title,
        'description': description,
        'tags': tags,
        'duration': duration_minutes * 60
    }

    with open('metadata.json', 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    
    print(f"Metadata generated: {metadata}")
    return metadata

def refresh_token():
    creds = None
    token_path = 'token.json'
    client_secrets_path = 'client_secrets.json'

    if not os.path.exists(client_secrets_path):
        print("Error: client_secrets.json file not found.")
        return None

    with open(client_secrets_path, 'r') as f:
        client_secrets = json.load(f)

    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
            refresh_token = token_data.get('refresh_token')
            token_uri = token_data.get('token_uri')
            client_id = token_data.get('client_id')
            client_secret = token_data.get('client_secret')

        if refresh_token:
            creds = Credentials(
                None, 
                refresh_token=refresh_token,
                token_uri=token_uri,
                client_id=client_id,
                client_secret=client_secret,
                scopes=SCOPES
            )

    if creds and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
            print("Token refreshed successfully.")
        except RefreshError as e:
            print(f"Error refreshing token. Token might be invalid. Reauthorizing...")
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
        print("New token generated and saved.")
    
    return creds

def upload_to_youtube(video_file, metadata):
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
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")

def main():
    used_content = load_used_content()

    if '--auto' in sys.argv:
        with open('auto.json', 'r') as f:
            config = json.load(f)

        if config['videos']:
            video_config = config['videos'].pop(0)
            duration_minutes = video_config['duration_minutes']
            video_query = video_config['video_query']
            audio_query = video_config['audio_query']
            should_upload_to_youtube = video_config['upload_to_youtube']

            video_url = search_and_download_meditation_video(used_content['videos'], video_query)
            if video_url:
                used_content['videos'].append(video_url)

            audio_url, attribution_text = search_and_download_music(audio_query, used_content['audios'])
            if audio_url:
                used_content['audios'].append(audio_url)

            save_used_content(used_content)

            metadata = generate_metadata(video_query, duration_minutes, attribution=attribution_text)

            combine_audio_video("video.mp4", "music.mp3", "final_video.mp4", duration_minutes=duration_minutes)

            if should_upload_to_youtube:
                refresh_token()
                upload_to_youtube("final_video.mp4", metadata)

            with open('auto.json', 'w') as f:
                json.dump(config, f, indent=4)
        else:
            print("All video configurations have been processed.")

    else:
        while True:
            duration_minutes = int(input("Enter the duration for the video (in minutes): "))
            video_query = input("Enter the search query for the Pixabay video: ")
            audio_query = input("Enter the search query for the Freesound music: ")

            video_url = search_and_download_meditation_video(used_content['videos'], video_query)
            if video_url:
                used_content['videos'].append(video_url)

            audio_url, attribution_text = search_and_download_music(audio_query, used_content['audios'])
            if audio_url:
                used_content['audios'].append(audio_url)

            while True:
                user_input = input("\nReview the downloaded video and music. Please select an option. \n1) Proceed to making the final video \n2) Download a new video \n3) Download new music \n4) Download a new video and music\n").lower()

                if user_input == '1':
                    break
                elif user_input == '2':
                    video_url = search_and_download_meditation_video(used_content['videos'])
                    if video_url:
                        used_content['videos'].append(video_url)
                elif user_input == '3':
                    audio_url, attribution_text = search_and_download_music("rain thunder", used_content['audios'])
                    if audio_url:
                        used_content['audios'].append(audio_url)
                elif user_input == '4':
                    video_url = search_and_download_meditation_video(used_content['videos'])
                    if video_url:
                        used_content['videos'].append(video_url)
                    audio_url, attribution_text = search_and_download_music("rain thunder", used_content['audios'])
                    if audio_url:
                        used_content['audios'].append(audio_url)

            save_used_content(used_content)

            metadata = generate_metadata(video_query, duration_minutes, attribution=attribution_text)

            combine_audio_video("video.mp4", "music.mp3", "final_video.mp4", duration_minutes=duration_minutes)

            upload_choice = input("Do you want to upload the video to YouTube? (yes/no): ").lower()
            if upload_choice == 'yes':
                refresh_token()
                upload_to_youtube("final_video.mp4", metadata)

            repeat = input("Do you want to create another video? (yes/no): ").lower()
            if repeat != 'yes':
                break

if __name__ == "__main__":
    main()