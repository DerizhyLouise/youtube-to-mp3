from pytubefix import YouTube, Playlist
import os
import moviepy.editor as mp
import re

output_folder = "./converted/"
os.makedirs(output_folder, exist_ok=True)

playlist_url = input("Enter Youtube Plasylist URL: ")
playlist = Playlist(playlist_url)

print(f"Found {len(playlist.video_urls)} videos in the playlist.")

# Download audio
for url in playlist.video_urls:
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        
        if not audio_stream:  # If no MP4 available, fall back to any available format
            audio_stream = yt.streams.get_audio_only()

        if audio_stream:
            print(f"Downloading: {yt.title}")
            audio_stream.download(output_folder)
        else:
            print(f"Skipping {yt.title}: No audio stream found.")
    except Exception as e:
        print(f"Skipping {url}: {e}")

# Rename M4A to MP4
for file in os.listdir(output_folder):
    if file.endswith(".m4a"):
        old_path = os.path.join(output_folder, file)
        new_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".mp4")
        os.rename(old_path, new_path)

# Convert to MP3
for file in os.listdir(output_folder):
    if file.endswith(".mp4"):  # Also works for renamed M4A
        mp4_path = os.path.join(output_folder, file)
        mp3_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".mp3")

        try:
            print(f"Converting: {file}")
            audio_clip = mp.AudioFileClip(mp4_path)
            audio_clip.write_audiofile(mp3_path)
            audio_clip.close()
            os.remove(mp4_path)
        except Exception as e:
            print(f"Error converting {file}: {e}")

print("Download and conversion complete!")
