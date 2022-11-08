import os

from dotenv import load_dotenv

from src.toggl import Toggl

load_dotenv()

CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOGGL_API = os.getenv("TOGGL_API")


class TestToggl:
    def test_get_workspace_ids(self):
        toggl = self.get_toggl()
        test_data = [{"id": 12345, "organization_id": 12345, "name": "test"}]
        workspace_ids = toggl.get_workspace_ids(test_data)
        assert workspace_ids == [12345]

    def test_get_projects_ids(self):
        toggl = self.get_toggl()
        data = [
            {
                "id": 123,
                "workspace_id": 123456789,
            },
            {
                "id": 456,
                "workspace_id": 987,
            },
        ]
        projects_ids = toggl.get_projects_ids(data)
        assert projects_ids == [123, 456]

    def test_get_item_time_in_project(self):
        project_data = {
            "total_grand": 3803000,
            "total_billable": None,
            "total_currencies": [{"currency": None, "amount": None}],
            "data": [
                {
                    "id": 186798029,
                    "title": {
                        "project": "English",
                        "client": None,
                        "color": "0",
                        "hex_color": "#d92b2b",
                    },
                    "time": 3803000,
                    "total_currencies": [{"currency": None, "amount": None}],
                    "items": [
                        {
                            "title": {"time_entry": "English Grammar in Use"},
                            "time": 3803000,
                            "cur": None,
                            "sum": None,
                            "rate": None,
                            "local_start": "2022-11-01T17:48:39",
                        }
                    ],
                }
            ],
        }
        toggl = self.get_toggl()
        time = toggl.get_item_time_in_project(project_data)
        assert time == {"English": {"English Grammar in Use": "1:03:23"}}

    @staticmethod
    def get_toggl() -> Toggl:
        return Toggl(TOGGL_API)
