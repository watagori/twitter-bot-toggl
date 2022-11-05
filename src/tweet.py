import datetime
import os

import tweepy

from toggl import Toggl

consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
toggl_api = os.environ.get("TOGGL_API")


def get_toggl_message():
    item_time = {}
    toggl = Toggl(toggl_api)
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
    tweet_message = f"Today({get_today()})'s Activities:\n"
    for key, value in toggl_message.items():
        tweet_message += f"{key} {value}\n"
    tweet_message += "#WatagoriActivity"
    return tweet_message


def tweet():
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    client.create_tweet(text=str(create_tweet_message()))


if __name__ == "__main__":
    tweet()
