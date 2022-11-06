import datetime
import os

import tweepy

from toggl import Toggl

CONSUMER_KEY = os.environ.get("API_KEY")
CONSUMER_SECRET = os.environ.get("API_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
TOGGL_API = os.environ.get("TOGGL_API")


def get_toggl_message():
    item_time = {}
    print(f"TOGGL_API: {TOGGL_API}")
    toggl = Toggl(TOGGL_API)
    workspace_id = toggl.get_workspace_id()
    projects_id = toggl.get_projects_id(workspace_id[0])
    today = get_today()
    yesterday = get_yesterday()

    for project_id in projects_id:
        project_data = toggl.get_projects_data(
            yesterday, today, workspace_id[0], project_id
        )

        item_time.update(toggl.get_item_time_in_project(project_data))
    return item_time


def get_today():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d")


def get_yesterday():
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def create_tweet_message():
    toggl_message = get_toggl_message()
    tweet_message = f"{get_yesterday()} Activities:\n"
    for key, value in toggl_message.items():
        tweet_message += f"{key} {value}\n"
    tweet_message += "#WatagoriActivity"
    return tweet_message


def tweet():
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    client.create_tweet(text=str(create_tweet_message()))


if __name__ == "__main__":
    tweet()
