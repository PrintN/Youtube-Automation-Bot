# YouTube Automation Bot

This Python-based bot automates the creation and upload of YouTube videos by sourcing content from Pixabay and Freesound. It uses GitHub Actions to run daily, creating and uploading fresh videos automatically without manual input. Check out the automated [Youtube channel](https://www.youtube.com/@ReIaxingSleepMusic).

![GitHub License](https://img.shields.io/github/license/PrintN/Youtube-Automation-Bot)
![GitHub Issues](https://img.shields.io/github/issues-raw/PrintN/Youtube-Automation-Bot)
![GitHub Fork](https://img.shields.io/github/forks/PrintN/Youtube-Automation-Bot)

## Features

- **Automated Video Search & Download**: Fetches relevant video clips from Pixabay based on user-defined search queries.
- **Music Search & Download**: Downloads music from Freesound with proper attribution for Creative Commons-licensed content.
- **Video Creation**: Combines video and audio into a final video, customizable for durations like 30, 60, or 90 minutes.
- **Automated YouTube Upload**: Uses the YouTube Data API to upload the final video directly to a YouTube channel.
- **Daily Automation**: Can be configured to run automatically with GitHub Actions, generating and uploading a new video every day.

## Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- API keys for [Pixabay](https://pixabay.com/api/docs/) and [Freesound](https://freesound.org/home/login/?next=/apiv2/apply)
- YouTube Data API access ([YouTube API Setup Guide](https://www.youtube.com/watch?v=aFwZgth790Q))


## Setup

<details>
  <summary>Setup (Manual Use)</summary>

Clone the repository to your machine:
```bash
git clone https://github.com/PrintN/Youtube-Automation-Bot
cd Youtube-Automation-Bot
```

Run the setup.
```bash
python3 setup.py
```
This will: 
1. Install required packages
2. Ask for Pixabay, Freesound, Google Client ID, and Secret
3. Open a window for YouTube channel authorization
4. Reset auto.json and used_content.json

### Usage
Run main.py manually to generate videos interactively:

```bash
python main.py
```
</details>

<details>
  <summary>Setup (Automated with Github Actions)</summary>
  
#### Start by [forking](https://github.com/PrintN/Youtube-Automation-Bot/fork) this repo.

Clone the repository to your machine:
```bash
git clone https://github.com/YOUR-FORKED-REPO
cd Youtube-Automation-Bot
```

```bash
python3 setup.py
```
This will: 
1. Install required packages
2. Ask for Pixabay, Freesound, Google Client ID, and Secret
3. Open a window for YouTube channel authorization
4. Reset auto.json and used_content.json

### Configuring API Keys

To enable the bot to run daily using GitHub Actions, you'll need to add the following secrets to your GitHub repository:

1. Go to: ```Settings > Secrets and variables > Actions``` in your forked repo.
2. Click "New repository secret" and add the following secrets:

   - **FREESOUND_API_KEY**: Your Freesound API key.
   - **PIXABAY_API_KEY**: Your Pixabay API key.
   - **CLIENT_SECRETS_JSON**: Base64-encoded ```client_secrets.json``` file.
   - **TOKEN_JSON**: Base64-encoded ```token.json``` file.

#### How to Base64 Encode Files:
- **Linux/macOS**:
  ```bash
  base64 client_secrets.json > encoded_client_secrets.txt
  base64 token.json > encoded_token.txt
  ```
- **Windows (Powershell)**  
  ```poweshell
  [Convert]::ToBase64String([IO.File]::ReadAllBytes("client_secrets.json")) > encoded_client_secrets.txt
  [Convert]::ToBase64String([IO.File]::ReadAllBytes("token.json")) > encoded_token.txt
  ```
Copy the contents of ```encoded_client_secrets.txt``` and ```encoded_token.txt``` into the value fields for **CLIENT_SECRETS_JSON** and **TOKEN_JSON**.

### Configuring auto.json
This file contains video configurations for the bot to run in auto mode. You can create as many videos configuration as you want. Example structure:
```json
{
  "videos": [
      {
          "duration_minutes": 30,
          "video_query": "forest landscapes",
          "audio_query": "forest ambiance",
          "upload_to_youtube": false,
          "video_type": "video"
      },
      {
          "duration_minutes": 0.55,
          "video_query": "mountain sunrise",
          "audio_query": "gentle wind",
          "upload_to_youtube": true,
          "video_type": "short"
      },
  ]
}
```
### Adjusting the Schedule
To change the bot’s schedule, edit ```.github/workflows/daily-video.yaml```:
```yaml
on:
  schedule:
    - cron: 0 5 * * * # 05:00 AM UTC
```
</details>

## Limitations of the Youtube API
By default, users are allowed to upload videos with a maximum duration of 15 minutes. If you wish to upload videos that exceed this limit, you will need to verify your account. For more details click [here](https://support.google.com/youtube/answer/71673).

## ⭐ Support the Project
If you find this project helpful, please consider giving it a ⭐! Starring the repository helps others discover the project and motivates further development. Thank you for your support!

## Ideas for Your Channel
Here are some content ideas for an automated YouTube channel you could do by modifying the bot:
- **Relaxing Sleep/Meditation Videos (Current)**
- **Motivational Quotes**
- **Meme Compilations**
- **Music Lyrics Videos**
- **Reddit Post Discussions**

## License
This project is licensed under the [MIT License](LICENSE).