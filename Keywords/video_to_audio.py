import moviepy.editor as mp

def convert_video_to_audio(video_file, audio_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)