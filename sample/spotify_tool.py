import config
import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import time


def get_token(username, scope, client_id, client_secret, redirect_url="http://google.com/"):
    # Erase cache and prompt for user permission:
    try:
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_url)
    except (AttributeError, JSONDecodeError):
        os.remove(".cache-" + username)
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_url)
    return token


def create_spotify_object(token):
    spotify_object = spotipy.Spotify(auth=token)
    return spotify_object


# Functions to get current music information:
def get_art_url(spotify_object):
    return spotify_object.current_user_playing_track()['item']['album']['images'][0]["url"]


# returns song as string
def get_song(spotify_object):
    return spotify_object.currently_playing()["item"]["name"]


# returns artist as string
def get_artist(spotify_object):
    return spotify_object.currently_playing()["item"]["artists"][0]["name"]


def get_track_url(spotify_object):
    return spotify_object.currently_playing()['item']['external_urls']['spotify']


def skip_current_track(spotify_object):
    spotify_object.next_track()


# Lays out the code flow, runs sample if called directly
def main():
    # Gives Spotify credentials:
    current_username = config.spotify_username
    current_scope = "user-read-currently-playing user-modify-playback-state"

    # Gives developer app credential:
    current_client_id = config.spotify_dev_id
    current_secret = config.spotify_dev_secret

    token = get_token(current_username, current_scope, current_client_id, current_secret)

    sp = create_spotify_object(token)

    print(get_art_url(sp))
    print(get_song(sp))
    print(get_artist(sp))
    print(get_track_url(sp))

    # Skips current track
    time.sleep(4)
    skip_current_track(sp)


# runs main (sample) if called directly
if __name__ == '__main__':
    main()
