import json

def generate_metadata(query, duration_minutes, attribution=None, is_short=False):
    clean_query = query.replace("AI generated", "").strip()
    if is_short:
        title = f"Relaxing {clean_query.capitalize()} Music #shorts"
    else:
        title = f"Relaxing {clean_query.capitalize()} Music ({duration_minutes} minutes)"
    description = (
        f"Welcome to this {duration_minutes}-minute {clean_query} video, created to help you find calm and relaxation. "
        "Enjoy soothing music combined with peaceful visuals, perfect for meditation, relaxation, and sleep.\n\n"
        "Whether you're unwinding after a long day or looking to enhance your meditation practice, this video is here to provide peace and serenity."
    )
    
    if attribution:
        description += f"\n\n🎶 Music Attribution 🎶\n{attribution}"
    
    description += (
        "\n-------------------------------------------------------------------------------------\n"
        "📽️ This video was created by the YouTube Automation Bot."
        " Check out the project here 👉 https://github.com/PrintN/Youtube-Automation-Bot.\n"
    )
    
    tags = [clean_query, "relaxation", "calm", "soothing music", "meditation", "sleep", "stress relief", "mindfulness"]
    
    if '.' in str(duration_minutes):
        minutes, seconds = str(duration_minutes).split('.')
        minutes = str(minutes)
        seconds = str(seconds)
    else:
        minutes = str(duration_minutes)
        seconds = str("0")

    metadata = {
        'title': title,
        'description': description,
        'tags': tags,
        'duration': minutes + "." + seconds
    }

    with open('metadata.json', 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    return metadata