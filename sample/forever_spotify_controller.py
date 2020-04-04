import spotify_controller
import time


# make it so this all runs in one script with nested loops
# make it not print message every 15 seconds
# ADD EMAIL SENDING ON WAIT=1
# Create log of every time it tries to start it
# add an error count tracker that sends an email after a certain amount of errors?
# make forever reusable with arguments?


print("\n[forever_spotify_controller] Starting spotify_controller.py")
while 1:
    # checks if any music is playing
    try:
        spotify_controller.main()
    # waits if no music is playing
    except TypeError:
        print("[forever_spotify_controller] No songs currently playing. Waiting...")
        time.sleep(25)
    except Exception as e:
        print("[forever_spotify_controller] The error: '" + str(e) +
              "' occurred while running spotify_controller.py. Trying again...")
        time.sleep(30)
