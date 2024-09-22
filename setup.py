import os
import subprocess
from pathlib import Path
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        exit(1)

def setup_api():
    pixabay_api_key = input("Enter your Pixabay API Key: ")
    freesound_api_key = input("Enter your Freesound API Key: ")

    env_path = Path(".env")
    
    env_content = {}
    if env_path.exists():
        with env_path.open('r') as env_file:
            for line in env_file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_content[key] = value

    env_content['PIXABAY_API_KEY'] = pixabay_api_key
    env_content['FREESOUND_API_KEY'] = freesound_api_key

    with env_path.open('w') as env_file:
        for key, value in env_content.items():
            env_file.write(f"{key}={value}\n")

    print(f".env file updated successfully at {env_path.resolve()}")

    client_id = input("Enter your Google Client ID: ")
    client_secret = input("Enter your Google Client Secret: ")

    client_secrets_path = Path("client_secrets.json")

    client_secrets = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token"
        }
    }

    with client_secrets_path.open('w') as json_file:
        json.dump(client_secrets, json_file, indent=4)

    print(f"client_secrets.json created/updated successfully at {client_secrets_path.resolve()}")

def setup_youtube_token():
    print("Setting up YouTube API credentials...")

    creds = None
    token_path = Path("token.json")

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with token_path.open('w') as token_file:
            token_file.write(creds.to_json())

    print(f"token.json created/updated successfully at {token_path.resolve()}")

def reset_files():
    auto_json_path = Path("auto.json")
    used_content_path = Path("used_content.json")

    auto_default = {
        "videos": []
    }
    used_content_default = {
        "videos": [],
        "audios": []
    }

    with auto_json_path.open('w') as auto_file:
        json.dump(auto_default, auto_file, indent=4)
    print(f"auto.json reset to default at {auto_json_path.resolve()}")

    with used_content_path.open('w') as used_file:
        json.dump(used_content_default, used_file, indent=4)
    print(f"used_content.json reset to default at {used_content_path.resolve()}")

def main():
    print("Setting up the project...")
    
    # Step 1: Install requirements
    install_requirements()

    # Step 2: Setup API keys
    setup_api()

    # Step 3: Setup YouTube token
    setup_youtube_token()

    # Step 4: Reset auto.json and used_content.json
    reset_files()

    print("Setup complete! You're ready to run your program.")

if __name__ == "__main__":
    main()