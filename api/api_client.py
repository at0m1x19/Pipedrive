import os

import requests
from dotenv import load_dotenv

load_dotenv()


class PipedriveClient:
    def __init__(self):
        self.token = os.getenv("PIPEDRIVE_API_TOKEN")
        if not self.token:
            raise ValueError("PIPEDRIVE_API_TOKEN is not set in .env or environment variables.")
        self.base_url = "https://api.pipedrive.com/v1"
        self.session = requests.Session()

    def _request(self, method, endpoint, **kwargs):
        """Helper to append api_token to query params and make the HTTP request."""
        url = f"{self.base_url}{endpoint}"
        params = kwargs.pop('params', {})
        params['api_token'] = self.token
        kwargs['params'] = params

        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def create_person(self, name, email=None, phone=None, org_id=None, label_ids=None):
        params = {
            "name": name,
            "email": email,
            "phone": phone,
            "org_id": org_id,
        }

        if label_ids:
            params["label_ids"] = label_ids

        resp = self._request("POST", "/persons", json=params)
        return resp.json()["data"]

    def get_person(self, person_id):
        resp = self._request("GET", f"/persons/{person_id}")
        return resp.json()["data"]

    def delete_person(self, person_id):
        resp = self._request("DELETE", f"/persons/{person_id}")
        return resp.json()

    def create_organization(self, name):
        data = {"name": name}
        resp = self._request("POST", "/organizations", json=data)
        return resp.json()["data"]

    def delete_organization(self, org_id):
        resp = self._request("DELETE", f"/organizations/{org_id}")
        return resp.json()
