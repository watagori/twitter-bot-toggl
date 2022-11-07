import base64

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

    def get_workspace_id(self):
        url_workspace_id = f"{self.api_url}/workspaces"
        try:
            response_workspace_id = requests.get(
                url_workspace_id, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        workspace_id = list(map(lambda x: x["id"], response_workspace_id))
        return workspace_id

    def get_projects_id(self, workspace_id):
        url_projects_id = f"{self.api_url}/workspaces/{workspace_id}/projects"
        try:
            response_projects_id = requests.get(
                url_projects_id, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        projects_id = list(map(lambda x: x["id"], response_projects_id))
        return projects_id

    def get_projects_data(self, from_date, to_date, workspace_id, projects_id):
        url = (
            f"{self.api_url_reports}/summary?workspace_id={workspace_id}&since={from_date}&until="
            f"{to_date}&project_ids={projects_id}&user_agent=api_test"
        )
        try:
            response = requests.get(url, headers=self.headers).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response

    def get_item_time_in_project(self, projects_data):
        item_time = {}
        if projects_data["total_grand"] is not None:
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

        return item_time
