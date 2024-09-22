# YouTube Automation Bot

This Python-based bot automates the creation and upload of YouTube videos by sourcing content from Pixabay and Freesound. It uses GitHub Actions to run daily, creating and uploading fresh videos automatically without manual input. Checkout the automated [Youtube channel](https://www.youtube.com/@ReIaxingSleepMusic).

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
- [Pixabay](https://pixabay.com/api/docs/) and [Freesound](https://freesound.org/home/login/?next=/apiv2/apply) API keys
- YouTube Data API access ([How to set up Youtube API on Google Cloud](https://www.youtube.com/watch?v=aFwZgth790Q))

## Setup (Manual Use)

Clone the repository:
```bash
git clone https://github.com/PrintN/Youtube-Automation-Bot
cd Youtube-Automation-Bot
```

```bash
python3 setup.py
```
It will 
```
1. Download all the pip packages necessary 
2. Ask you for your Pixabay and Freesound API keys.
3. Ask you for your Google Client ID and Google Client Secret
4. Open a new window and ask you to authorize your Youtube channel.
5. Reset auto.json and used_content.json
```

### Usage
Manual Mode:
Run main.py manually to generate videos interactively:

```bash
python main.py
```

## Setup Github Actions (Automated)
Start by [forking](https://github.com/PrintN/Youtube-Automation-Bot) this repo.

Clone the repository:
```bash
git clone https://github.com/YOUR-FORKED-REPO
cd Youtube-Automation-Bot
```

```bash
python3 setup.py
```
It will 
```
1. Download all the pip packages necessary 
2. Ask you for your Pixabay and Freesound API keys.
3. Ask you for your Google Client ID and Google Client Secret
4. Open a new window and ask you to authorize your Youtube channel.
5. Reset auto.json and used_content.json
```
### Configuring API keys
This bot can run daily using GitHub Actions. See the workflow.yaml file.

Make sure you are inside the forked repo and go to Settings > Secrets and variables > Actions then click on the "New repository secret" button. You'll have to make 4 secrets:
```bash
FREESOUND_API_KEY
PIXABAY_API_KEY
CLIENT_SECRETS_JSON
TOKEN_JSON
```
The Freesound and Pixabay API keys you just paste them in the value field. For the CLIENT_SECRETS_JSON and TOKEN_JSON you'll have to paste the base64 encoded version of them.

### Configuring auto.json
This file contains video configurations for the bot to run in auto mode. You can create as many videos configuration as you want. Example structure:
```json
{
  "videos": [
    {
      "duration_minutes": 60,
      "video_query": "meditation",
      "audio_query": "calm music",
      "upload_to_youtube": true
    },
    {
      "duration_minutes": 30,
      "video_query": "nature",
      "audio_query": "soft rain",
      "upload_to_youtube": false
    }
  ]
}
```
### Setting the time the bot will run
To set the time go to .github > /workflows/ > daily-video.yaml. And change this:
```yaml
on:
  schedule:
    - cron: 0 5 * * * # 05:00 AM UTC
```

## Ideas
Here are some content ideas for an automated YouTube channel you could do by modifying the bot:
- **Relaxing Sleep/Meditation Videos (Current)**
- **Motivational Quotes**
- **Meme Compilations**
- **Music Lyrics Videos**
- **Reddit Post Discussions**

## License
This project is licensed under the [MIT License](LICENSE).