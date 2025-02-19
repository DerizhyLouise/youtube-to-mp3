from pytubefix import YouTube, Playlist
import os
import moviepy.editor as mp
import re

def download_single_video():
    url = input("Enter the URL of the video you want to download: \n>> ")
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    
    print("Enter the destination (leave blank for current directory)")
    destination = str(input(">> ")) or '.'
    
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    print(f"{yt.title} has been successfully downloaded as MP3.")

def download_playlist():
    output_folder = "./converted/"
    os.makedirs(output_folder, exist_ok=True)
    
    playlist_url = input("Enter YouTube Playlist URL: ")
    playlist = Playlist(playlist_url)
    
    print(f"Found {len(playlist.video_urls)} videos in the playlist.")
    
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

if __name__ == "__main__":
    print("Select an option:")
    print("1. Download a single video")
    print("2. Download an entire playlist")
    choice = input(">> ")
    
    if choice == "1":
        download_single_video()
    elif choice == "2":
        download_playlist()
    else:
        print("Invalid choice. Exiting.")
