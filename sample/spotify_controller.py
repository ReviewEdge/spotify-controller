import config
import spotify_bridge
import sheets
import date_convert
import use_files
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
    token = spotify_bridge.get_token(username, scope, ID, SECRET, URI)
    spot_object = spotify_bridge.create_spotify_object(token)

    # Google Sheets Authentication
    service = sheets.authenticate_sheets_api()
    # Song log sheet:
    song_log_sheet_id = config.song_log_sheet_id
    # Blacklist sheet:
    blacklist_sheet_id = config.blacklist_sheet_id

    print("\n[save_played_songs] Starting Song Logger...")

    print("\n[save_played_songs] Getting latest version of blacklist...")

    # downloads latest blacklist from google sheet
    blacklist_raw = sheets.get_all_sheets_data(service, blacklist_sheet_id, "A:B")
    blacklist = []
    for i in blacklist_raw:
        blacklist.append(i[0])

    # finds last song saved to google sheet database
    if use_files.basic_read_file("last_recorded_song") == "FILE NOT FOUND":
        last_recorded_song = "this is a nonexistent song title"
    else:
        last_recorded_song = use_files.basic_read_file("last_recorded_song")

    while 1:
        latest_song = spotify_bridge.get_song(spot_object)

        # Skips songs on blacklist
        if latest_song in blacklist:
            print("[save_played_songs] Found blacklisted song: '" + latest_song + "'. Skipping...")
            spotify_bridge.skip_current_track(spot_object)

        elif latest_song != last_recorded_song:
            latest_artist = spotify_bridge.get_artist(spot_object)
            sheets.write_data_list_to_sheet(service, song_log_sheet_id, "A:D", [latest_song, latest_artist,
                                                                               date_convert.get_readable("day"),
                                                                               date_convert.get_readable_time()])
            last_recorded_song = latest_song

            # Logs last recorded song to file so it's not acted on the next time the script is run:
            use_files.basic_write_file("last_recorded_song", last_recorded_song)

            print("[save_played_songs] Recorded: " + latest_song + " by " + latest_artist)

            # extra wait time, assumes song was just changed
            time.sleep(12)

        # Waits if song hasn't changed
        else:
            time.sleep(8)


# runs main if called directly
if __name__ == '__main__':
    main()
