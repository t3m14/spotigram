import requests

def single_track(artist, name):
    url = "https://www.spotifydl.xyz/api/download?name="+ name +"&artist="+ artist
r = requests.post(url, data=data).text