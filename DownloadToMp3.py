import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
from os.path import exists


def authenticate_user():
    cid = 'fe4c13fe27584c0591d2db5e5ac7a2f2'
    secret = '96943fdde9214d1abd16fe74296f1a00'
    
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

def get_spotify_track_list(sp, playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_info = [[x["track"]["name"], x["track"]["artists"][0]['name']] for x in sp.playlist_tracks(playlist_URI)["items"]]
    return track_info

def get_youtube_link(song_name):
    videosSearch = VideosSearch(song_name, limit = 1)
    return videosSearch.result()['result'][0]['link']

def download_song(song_name):
    song_name = track[0] + ' - ' + track[1]
    print('Downloading Song:', song_name[:30])

    file_exists = exists('./Downloads/' + song_name + '.mp3')

    if not file_exists:
        video_link = get_youtube_link(song_name)
        video = YouTube(video_link)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"./Downloads/{song_name}.mp3")
        print('Downloading Complete')
    else:
        print('Downloading Skipped (File Already Exists)', song_name[:30])

if __name__ == '__main__':
    sp = authenticate_user()
    playlist_link = "https://open.spotify.com/playlist/1qWvDCQdddS63Z8sFPJKXs"
    track_names = get_spotify_track_list(sp, playlist_link)

    for track in track_names[:10]:
        try:
            download_song(track)
        except KeyError:
           print("Unable to Download Song:", track[0])
