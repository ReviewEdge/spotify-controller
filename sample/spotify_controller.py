import config
import spotify_tool
import gsheets_tool
from furtherpy.sample import files_tool
from furtherpy.sample import date_conv_tool
import time


def main():
    # Gives Spotify credentials:
    username = config.spotify_username
    scope = "user-read-currently-playing"

    # Gives developer app credential:
    ID = config.spotify_dev_id
    SECRET = config.spotify_dev_secret
    URI = "http://google.com/"

    # Spotipy Authentication
    token = spotify_tool.get_token(username, scope, ID, SECRET, URI)
    spot_object = spotify_tool.create_spotify_object(token)

    # Google Sheets Authentication
    service = gsheets_tool.authenticate_sheets_api()
    # Song log sheet:
    song_log_sheet_id = config.song_log_sheet_id
    # Blacklist sheet:
    blacklist_sheet_id = config.blacklist_sheet_id

    print("\n[spotify_controller] Starting Song Logger...")

    print("\n[spotify_controller] Getting latest version of blacklist...")

    # downloads latest blacklist from google sheet
    blacklist_raw = gsheets_tool.get_all_sheets_data(service, blacklist_sheet_id, "A:B")
    blacklist = []
    for i in blacklist_raw:
        blacklist.append(i[0])

    # finds last song saved to google sheet database
    if files_tool.basic_read_file("last_recorded_song") == "FILE NOT FOUND":
        last_recorded_song = "this is a nonexistent song title"
    else:
        last_recorded_song = files_tool.basic_read_file("last_recorded_song")

    while 1:
        latest_song = spotify_tool.get_song(spot_object)

        # Skips songs on blacklist
        if latest_song in blacklist:
            print("[spotify_controller] Found blacklisted song: '" + latest_song + "'. Skipping...")
            spotify_tool.skip_current_track(spot_object)

        elif latest_song != last_recorded_song:
            latest_artist = spotify_tool.get_artist(spot_object)
            gsheets_tool.write_data_list_to_sheet(service, song_log_sheet_id, "A:D", [latest_song, latest_artist,
                                                                               date_conv_tool.get_readable("day"),
                                                                               date_conv_tool.get_readable_time()])
            last_recorded_song = latest_song

            # Logs last recorded song to file so it's not acted on the next time the script is run:
            files_tool.basic_write_file("last_recorded_song", last_recorded_song)

            print("[spotify_controller] Recorded: " + latest_song + " by " + latest_artist)

            # extra wait time, assumes song was just changed
            time.sleep(12)

        # Waits if song hasn't changed
        else:
            time.sleep(8)


# runs main if called directly
if __name__ == '__main__':
    main()
