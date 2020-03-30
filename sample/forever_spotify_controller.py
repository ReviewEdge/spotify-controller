import save_played_songs
import time


# make it so this all runs in one script with nested loops
# make it not print message every 15 seconds
# ADD EMAIL SENDING ON WAIT=1
# Create log of every time it tries to start it
# add an error count tracker that sends an email after a certain amount of errors?
# make forever reusable with arguments?


print("\n[forever_save_played_songs] Starting save_played_songs.py")
while 1:
    # checks if any music is playing
    try:
        save_played_songs.main()
    # waits if no music is playing
    except TypeError:
        print("[forever_save_played_songs] No songs currently playing. Waiting...")
        time.sleep(25)
    except Exception as e:
        print("[forever_save_played_songs] The error: '" + str(e) +
              "' occurred while running save_played_songs.py. Trying again...")
        time.sleep(30)
