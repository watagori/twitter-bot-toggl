import os

from dotenv import load_dotenv

from src import tweet

# from freezegun import freeze_time


load_dotenv()

CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOGGL_API = os.getenv("TOGGL_API")


class TestTweet:
    # @freeze_time("2022-11-09")
    # def test_get_toggl_message(self):
    #     data = tweet.get_toggl_message()
    #     test_data = {
    #         "English": {
    #             "English Grammar in Use": "1:13:44",
    #             "English Vocabulary": "1:46:52",
    #             "Native Camp": "0:29:15",
    #         },
    #         "Life": {"Walking/Running": "0:44:53"},
    #         "NII": {"Research": "4:54:54"},
    #         "PhD": {"Economics": "2:30:41"},
    #         "Sleep": {"Nap": "0:44:20", "Sleep": "7:50:41"},
    #     }
    #     assert data == test_data

    def test_create_message(self):
        test_message = {
            "Life": {"Walking/Running": "0:44:53"},
            "NII": {"Research": "4:54:54"},
        }
        message = tweet.create_tweet_message(test_message)
        assert (
            message
            == "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n[NII]\nResearch: 4:54:54\n#WatagoriActivity"
        )

    def test_words_count_under_280(self):
        test_message = "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n[NII]\nResearch: 4:54:54\n#WatagoriActivity"
        counter = tweet.words_count(test_message)
        assert counter is True

    def test_words_count_over_280(self):
        test_message = (
            "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n"
            "[NII]\nResearch: 4:54:54\n2022-11-08\n[Life]\n"
            "Walking/Running: 0:44:53\n[NII]\nResearch: 4:54:54\n"
            "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n[NII]\n"
            "Research: 4:54:54\n2022-11-08\n[Life]\nWalking/Running: 0:44:53\n"
            "[NII]\nResearch: 4:54:54\n#WatagoriActivity"
        )

        counter = tweet.words_count(test_message)
        assert counter is False

    def test_create_tweet_under_280(self):
        test_message = "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n[NII]\nResearch: 4:54:54\n#WatagoriActivity"
        message = tweet.create_tweet(test_message)
        assert message == test_message

    # def test_create_tweet_over_280(self):
    #     test_message = (
    #         "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n"
    #         "[NII]\nResearch: 4:54:54\n2022-11-08\n[Life]\n"
    #         "Walking/Running: 0:44:53\n[NII]\nResearch: 4:54:54\n"
    #         "2022-11-08\n[Life]\nWalking/Running: 0:44:53\n[NII]\n"
    #         "Research: 4:54:54\n2022-11-08\n[Life]\nWalking/Running: 0:44:53\n"
    #         "[NII]\nResearch: 4:54:54\n#WatagoriActivity"
    #     )
    #     message = tweet.create_tweet(test_message)
    #     assert message == test_message
