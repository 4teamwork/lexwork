import base64
import os
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class APIClient:
    def __init__(self, url, username, password):
        self.url = url.rstrip("/") + "/"
        self.session = requests.Session()
        retries = Retry(
            backoff_factor=1,
            status_forcelist=[429, 502, 503, 504],
            method_whitelist=frozenset(
                ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
            ),
        )
        self.session.mount(self.url, HTTPAdapter(max_retries=retries))
        self.session.headers.update(
            {"X-LEXWORK-LOGIN": username, "X-LEXWORK-PASSWORD": password}
        )

    def test(self):
        response = self._make_request("admin_interface/test.json")
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
                "data": str(base64.b64encode(file_like.read()), "utf-8"),
                "reason_for_signature": reason,
            }
        }
        response = self._make_request(
            "admin_interface/pdf_signature_jobs.json", "post", json=data
        )
        return response.json().get("result", {"signed_data": ""}).get("signed_data")

    def _make_request(self, path, verb="get", **kwargs):
        response = getattr(self.session, verb)(urljoin(self.url, path), **kwargs)
        response.raise_for_status()
        return response
