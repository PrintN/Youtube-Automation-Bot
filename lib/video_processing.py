from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx.all import audio_loop

def combine_audio_video(video_file, audio_file, output_file, duration_minutes=60, is_short=False):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    duration_seconds = duration_minutes * 60

    if is_short:
        video = video.resize((1080, 1920))

    video_loop = concatenate_videoclips([video] * (duration_seconds // int(video.duration) + 1)).subclip(0, duration_seconds)
    audio_looped = audio_loop(audio, duration=duration_seconds)
    
    final_video = video_loop.set_audio(audio_looped)
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

    video.close()
    audio.close()
    final_video.close()