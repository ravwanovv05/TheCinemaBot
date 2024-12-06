import yt_dlp
import webbrowser

Song = input("Enter the song name: ")
ydl_opts = {'quiet': True, 'default_search': 'ytsearch1'}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(Song, download=False)
    video_url = info['entries'][0]['webpage_url']
    webbrowser.open(video_url)
    print("Successfully Played!")
