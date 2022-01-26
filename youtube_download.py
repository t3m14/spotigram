import youtube_dl
from youtube_search import YoutubeSearch
import os
def download_mp3(text_to_search):
    attempts_left = 10
    best_url = None
    while attempts_left > 0:
        try:
            results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
            best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
            break
        except IndexError:
            attempts_left -= 1
            print("No valid URLs found for {}, trying again ({} attempts left).".format(
                text_to_search, attempts_left))
    if best_url is None:
        print("No valid URLs found for {}, skipping track.".format(text_to_search))
    # Run you-get to fetch and download the link's audio
    print("Initiating download for {}.".format(text_to_search))
    ydl_opts = {
        'outtmpl': 'downloaded_music/%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    info, track = '', ''
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info  = ydl.extract_info(best_url, download=False)
        track = str(info.get('id', None)) + '.mp3'
        if os.path.isfile('./downloaded_music/' + track)== True:
            print("EXISTS")
            return track
        else:
            print("NOT EXISTS")
            ydl.download([best_url])
            return track
