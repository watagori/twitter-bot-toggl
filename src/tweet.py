import datetime
import os

import tweepy
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

from toggl import Toggl

load_dotenv()

CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOGGL_API = os.getenv("TOGGL_API")


def get_toggl_message() -> dict:
    item_time = {}
    toggl = Toggl(TOGGL_API)
    workspace_id = toggl.get_workspace_ids(toggl.get_workspace_id_data())
    projects_id = toggl.get_projects_ids(toggl.get_projects_ids_data(workspace_id[0]))
    today = get_today()

    for project_id in projects_id:
        project_data = toggl.get_projects_data(
            today, today, workspace_id[0], project_id
        )

        item_time.update(toggl.get_item_time_in_project(project_data))
    return item_time


def create_tweet_message(message_data: dict) -> str:
    tweet_message = f"{get_today()}\n"
    for project_name, value in message_data.items():
        tweet_message += f"[{project_name}]\n"
        for item_name, time in value.items():
            tweet_message += f"{item_name}: {time}\n"
    tweet_message += "#WatagoriActivity"
    return tweet_message


def words_count(message: str) -> bool:
    if len(message) <= 280:
        return True
    else:
        return False


def create_tweet(message: str):
    if words_count(message):
        return message
    else:
        im = Image.new("RGB", (256, 410), (256, 256, 256))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("Arial", 14)
        draw.multiline_text((10, 10), message, fill=(0, 0, 0), font=font)
        im.save(f"data/tweet_{get_yesterday()}.png")


def tweet():
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    client.create_tweet(text=str(create_tweet_message(get_toggl_message())))


def get_today():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d")


def get_yesterday():
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


if __name__ == "__main__":
    tweet()
