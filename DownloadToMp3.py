import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
import ssl
import os
import subprocess


def convert_to_mp3(file, output):
    cmd = (
        'ffmpeg -i "%s"' % file
        + ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 "%s" > /dev/null 2>&1' % output
    )
    subprocess.call(cmd, shell=True)


def authenticate_user():
    cid = "fe4c13fe27584c0591d2db5e5ac7a2f2"
    secret = "96943fdde9214d1abd16fe74296f1a00"

    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def get_spotify_track_list(sp, playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    print("Getting Playlist Info")
    print("Playlist URI:", playlist_URI)
    print("Playlist Name:", sp.playlist(playlist_URI)["name"])
    print("Playlist Description:", sp.playlist(playlist_URI)["description"])

    results = sp.playlist_tracks(playlist_URI)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    track_info = [
        [x["track"]["name"], x["track"]["artists"][0]["name"]] for x in tracks
    ]

    return track_info


def get_youtube_link(song_name):
    videosSearch = VideosSearch(song_name, limit=1)
    return videosSearch.result()["result"][0]["link"]


def download_song(index, song_name, folder_name, total_songs):
    song_name = track[0] + " - " + track[1]
    print("Downloading Song:", song_name, f"({index+1}/{total_songs})")

    file_exists = os.path.exists(f"Downloads/{folder_name}/{song_name}.mp3")

    try:
        if not file_exists:
            video_link = get_youtube_link(song_name)
            video = YouTube(video_link)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(filename=f"Downloads/{folder_name}/{song_name}.wav")
            convert_to_mp3(
                f"Downloads/{folder_name}/{song_name}.wav",
                f"Downloads/{folder_name}/{song_name}.mp3",
            )

            os.remove(f"Downloads/{folder_name}/{song_name}.wav")
            print("Downloading Complete")
        else:
            print("Downloading Skipped - File Already Exists")
    except Exception as e:
        print("Downloading Skipped - Error Occurred")
        print(e)


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context

    sp = authenticate_user()
    folder_name = "Tech House"
    playlist_link = (
        "https://open.spotify.com/playlist/5ceLorHEjpOjqRbIFcUPa9?si=5a1beb0b6ee542ac"
    )
    track_names = get_spotify_track_list(sp, playlist_link)

    if not os.path.exists(f"Downloads/{folder_name}"):
        os.mkdir(f"Downloads/{folder_name}")

    for index, track in enumerate(track_names):
        try:
            download_song(index, track, folder_name, len(track_names))
        except KeyError:
            print("Unable to Download Song:", track[0])

    print("All Songs Downloaded")
    print("Total Songs Downloaded:", len(track_names))
