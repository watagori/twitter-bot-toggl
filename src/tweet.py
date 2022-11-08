import datetime
import os

import tweepy
from dotenv import load_dotenv

from toggl import Toggl

load_dotenv()

CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOGGL_API = os.getenv("TOGGL_API")


def get_toggl_message():
    item_time = {}
    toggl = Toggl(TOGGL_API)
    workspace_id = toggl.get_workspace_id()
    projects_id = toggl.get_projects_id(workspace_id[0])
    yesterday = get_yesterday()

    for project_id in projects_id:
        project_data = toggl.get_projects_data(
            yesterday, yesterday, workspace_id[0], project_id
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
    tweet_message = f"{get_yesterday()}\n"
    for project_name, value in toggl_message.items():
        tweet_message += f"[{project_name}]\n"
        for item_name, time in value.items():
            tweet_message += f"{item_name}: {time}\n"
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
