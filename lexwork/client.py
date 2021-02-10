import base64
import os
from urllib.parse import urljoin

import requests


class APIClient:
    def __init__(self, url, username, password):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(
            {"X-LEXWORK-LOGIN": username, "X-LEXWORK-PASSWORD": password}
        )

    def test(self):
        response = self.session.get(urljoin(self.url, "admin_interface/test.json"))
        return response

    def pdf_signature_reasons(self):
        response = self._make_request("admin_interface/pdf_signature_reasons.json")
        return response.json().get("result", [])

    def sign_pdf(self, file_like, reason, file_name=None):
        if not file_name:
            file_name = os.path.basename(file_like)
        data = {
            "pdf_signature_job": {
                "file_name": file_name,
                "data": base64.b64encode(file_like.read()),
                "reason_for_signature": reason,
            }
        }
        response = self._make_request(
            "admin_interface/pdf_signature_jobs.json", "post", json=data
        )
        return response.get("result", {"data": ""}).get("data")

    def _make_request(self, path, verb="get", **kwargs):
        response = getattr(self.session, verb)(urljoin(self.url, path), **kwargs)
        response.raise_for_status()
        return response
