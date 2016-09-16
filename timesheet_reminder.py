import os
import time
from slackclient import SlackClient
from time import gmtime, strftime

# Used 
# https://github.com/mattmakai/fullstackpython.com/blob/gh-pages/source/content/posts/160604-build-first-slack-bot-python.markdown
# For this bot

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

hour_lock = False

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Timesheet_Reminder connected and running!")
        while True:
            day = int(strftime("%d", gmtime()))
            hour = int(strftime("%H", gmtime()))
            minute = int(strftime("%M", gmtime()))
            
            if 11 < day < 16 or 26 < day < 31:
                if hour is 8 or hour is 12 or hour is 15:
                    if not hour_lock:
                        slack_client.api_call("chat.postMessage", channel="#beemon", text="Turn in your timesheet or don't get paid! :tada:",username='timesheet_reminder', icon_emoji=':robot_face:')
                        hour_lock = True
                else:
                    hour_lock = False
            time.sleep(READ_WEBSOCKET_DELAY)
            
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
