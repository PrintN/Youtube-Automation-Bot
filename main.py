import sys
sys.dont_write_bytecode = True
import json
from lib.content_handler import search_and_download_meditation_video, search_and_download_music, load_used_content, save_used_content
from lib.video_processing import combine_audio_video
from lib.youtube_upload import upload_to_youtube, refresh_token
from lib.metadata import generate_metadata
from lib.config import load_config

def main():
    used_content = load_used_content()

    if '--auto' in sys.argv:
        with open('auto.json', 'r') as f:
            config = json.load(f)

        video_created = False 

        while config['videos'] and not video_created:
            video_config = config['videos'].pop(0)
            video_query = video_config['video_query']
            audio_query = video_config['audio_query']
            should_upload_to_youtube = video_config['upload_to_youtube']
            video_type = video_config['video_type']
            duration_minutes = video_config['duration_minutes']

            is_short = video_type == 'short'

            video_url = search_and_download_meditation_video(used_content['videos'], video_query)
            if not video_url:
                print(f"Retrying with next config: Could not find a video for '{video_query}'")
                continue  

            used_content['videos'].append(video_url)

            audio_url, attribution_text = search_and_download_music(audio_query, used_content['audios'])
            if not audio_url:
                print(f"Retrying with next config: Could not find audio for '{audio_query}'")
                continue  

            used_content['audios'].append(audio_url)

            save_used_content(used_content)

            metadata = generate_metadata(video_query, duration_minutes, attribution=attribution_text, is_short=is_short)
            combine_audio_video("video.mp4", "music.mp3", "final_video.mp4", duration_minutes=duration_minutes, is_short=is_short)

            if should_upload_to_youtube:
                refresh_token()
                upload_to_youtube("final_video.mp4", metadata, is_short=is_short)

            with open('auto.json', 'w') as f:
                json.dump(config, f, indent=4)

            print(f"Successfully processed and uploaded video for query: '{video_query}'")
            video_created = True

        else:
            if not video_created:
                print("All video configurations have been processed or none were successful.")

    else:
        while True:
            video_type = input("Do you want to create a Short or a regular video? (Enter 'short' or 'video'): ")
            duration_minutes = float(input("Enter the duration for the video (in minutes): "))
            video_query = input("Enter the search query for the Pixabay video: ")
            audio_query = input("Enter the search query for the Freesound music: ")
            is_short = video_type == 'short'
            
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

            metadata = generate_metadata(video_query, duration_minutes, attribution=attribution_text, is_short=is_short)

            combine_audio_video("video.mp4", "music.mp3", "final_video.mp4", duration_minutes=duration_minutes, is_short=is_short)

            upload_choice = input("Do you want to upload the video to YouTube? (yes/no): ").lower()
            if upload_choice == 'yes':
                refresh_token()
                upload_to_youtube("final_video.mp4", metadata, is_short=is_short)

            repeat = input("Do you want to create another video? (yes/no): ").lower()
            if repeat != 'yes':
                break

if __name__ == "__main__":
    main()