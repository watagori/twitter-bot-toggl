import base64
from collections import defaultdict

import requests


class Toggl:
    def __init__(self, api_token):
        self.api_token = api_token
        self.api_url = "https://api.track.toggl.com/api/v9"
        self.api_url_reports = "https://api.track.toggl.com/reports/api/v2"
        self.headers = {
            "Authorization": "Basic "
            + base64.b64encode(bytes(api_token + ":api_token", "utf-8")).decode("utf-8")
        }

    def get_workspace_id_data(self) -> list:
        url_workspace_id = f"{self.api_url}/workspaces"
        try:
            response_workspace_id = requests.get(
                url_workspace_id, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response_workspace_id

    @staticmethod
    def get_workspace_ids(workspace_id_data: list) -> list:
        workspace_id = list(map(lambda x: x["id"], workspace_id_data))
        return workspace_id

    def get_projects_ids_data(self, workspace_id: int) -> list:
        url_projects_id = f"{self.api_url}/workspaces/{workspace_id}/projects"
        try:
            response_projects_id = requests.get(
                url_projects_id, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response_projects_id

    @staticmethod
    def get_projects_ids(projects_id_data: list) -> list:
        projects_ids = list(map(lambda x: x["id"], projects_id_data))
        return projects_ids

    def get_projects_data(
        self, from_date: str, to_date: str, workspace_id: int, projects_id: int
    ) -> dict:
        url = (
            f"{self.api_url_reports}/summary?workspace_id={workspace_id}&since={from_date}&until="
            f"{to_date}&project_ids={projects_id}&user_agent=WatagoriBot"
        )
        try:
            response = requests.get(url, headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    @staticmethod
    def get_item_time_in_project(projects_data: dict) -> dict:
        item_times = defaultdict(dict)
        item_time = {}
        if projects_data["data"]:
            project_name = projects_data["data"][0]["title"]["project"]
            for item in projects_data["data"][0]["items"]:
                seconds = item["time"] / 1000
                seconds = seconds % (24 * 3600)
                hour = seconds // 3600
                seconds %= 3600
                minutes = seconds // 60
                seconds %= 60
                item_time[item["title"]["time_entry"]] = "%d:%02d:%02d" % (
                    hour,
                    minutes,
                    seconds,
                )
                item_times[project_name] = item_time
        return item_times
