import requests
import json
import os

def get_playlist(playlist): 
   return json.loads(requests.get("https://www.spotifydl.xyz/api/playlist?id=" + playlist).text)


        
def download_track(name, artist):
    api_download_track = 'https://www.spotifydl.xyz/api/download?name={0}&artist={1}'.format(name, artist)
    file_name = str(artist) + ' - ' + str(name) + '.mp3'
    if os.path.isfile('./downloaded_music/' + file_name):
        print("EXISTS")
        return file_name
    else:
        print("NOT_EXISTS")
        track = requests.get(api_download_track, stream=True)
        if track.status_code == requests.codes.ok:
            with open('./downloaded_music/'+ file_name, 'wb') as a:
                a.write(track.content)
                #os.remove('./downloaded_music/' + file_name)
            return file_name    

        
