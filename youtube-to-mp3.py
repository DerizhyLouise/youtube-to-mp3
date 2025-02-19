from pytubefix import YouTube 
import os 
  
yt = YouTube( str(input("Enter the URL of the video you want to download: \n>> "))) 
  
video = yt.streams.filter(only_audio=True).first() 
  
print("Enter the destination (leave blank for current directory)") 
destination = str(input(">> ")) or '.'
  
out_file = video.download(output_path=destination) 
  
base, ext = os.path.splitext(out_file) 
new_file = base + '.mp3'
os.rename(out_file, new_file) 
  
print(yt.title + " has been successfully downloaded.")
