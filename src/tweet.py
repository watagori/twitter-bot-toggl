import os

import tweepy

from toggl import Toggl

consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_KEY_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
toggl_api = os.environ.get("TOGGL_API")


def toggl_message():
    item_time = {}
    toggl = Toggl(toggl_api)
    workspace_id = toggl.get_workspace_id()
    projects_id = toggl.get_projects_id(workspace_id[0])
    for project_id in projects_id:
        project_data = toggl.get_projects_data(
            "2022-11-01", "2022-11-6", workspace_id[0], project_id
        )

        item_time.update(toggl.get_item_time_in_project(project_data))
    return item_time


client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

client.create_tweet(text="test")
