import yt_dlp
import os
import json
import ctypes

def download(url: str):

    with open("config.json", "r") as f:
        config_data = json.load(f)
    config_data = config_data['config']

    # Makes a hidden dir
    folder_path = "temp"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x02)


    # Make sure ffmpeg path is correctly set for merging video and audio
    FFMPEG_PATH = os.path.join("C:", os.sep, "ffmpeg", "bin", "ffmpeg.exe")

    # yt-dlp configuration options
    ydl_opts = {
        'format': 'bestaudio/best',        # Select best video and best audio
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',      # The desired audio format
                'preferredquality': config_data['bitrate'],    # The desired bitrate
            },
            {
                # Embed metadata into the file
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                # Optional: Embed thumbnail as album art
                'key': 'EmbedThumbnail',
            },
        ],


        'writethumbnail': True, # Required if you want album art
        
        'ffmpeg_location': FFMPEG_PATH,              # Path to ffmpeg executable
        'outtmpl': 'temp/%(playlist_index)s.%(title)s.%(ext)s',              # Output file naming template
        'quiet': config_data['hide_download_progress'],                              # Show download progress
        'noplaylist': config_data['no_playlist']                           # Download only one video if playlist
    }

    # Example URL — Replace with your desired video link
    #video_url = 'https://www.youtube.com/watch?v=6S20mJvr4vs&list=OLAK5uy_mao9YHfZtBBTlxeT138lO0prcGHzNSWQM'

    # Start downloading
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print("DOWNLOAD COMPLETE")
    
    #Under here add somthing to pass it to metadata collecter
    dest_dir = config_data['output_dir']
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir('temp'):
        source_path = os.path.join('temp', filename)
        dest_path = os.path.join(dest_dir, filename)

        os.rename(source_path, dest_path)