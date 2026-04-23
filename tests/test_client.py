import base64
import io
import json
import unittest

from lexwork import APIClient


class Response:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload

    def raise_for_status(self):
        return None


class APIClientTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("https://lexwork.example.org", "user", "secret")
        self.requests = []

        def get(url, **kwargs):
            self.requests.append(("get", url, kwargs))
            return Response({"result": ["approval"]})

        def post(url, **kwargs):
            self.requests.append(("post", url, kwargs))
            return Response({"result": {"signed_data": "signed-pdf"}})

        self.client.session.get = get
        self.client.session.post = post

    def test_session_uses_json_accept_and_lexwork_credentials(self):
        self.assertEqual("application/json", self.client.session.headers["Accept"])
        self.assertEqual("user", self.client.session.headers["X-LEXWORK-LOGIN"])
        self.assertEqual("secret", self.client.session.headers["X-LEXWORK-PASSWORD"])

    def test_pdf_signature_reasons_uses_new_signer_api_endpoint(self):
        self.assertEqual(["approval"], self.client.pdf_signature_reasons())

        self.assertEqual(
            [
                (
                    "get",
                    "https://lexwork.example.org/api/signer/v1/pdf_signature_reasons",
                    {},
                )
            ],
            self.requests,
        )

    def test_sign_pdf_uses_new_signer_api_endpoint_and_json_payload(self):
        file_like = io.BytesIO(b"pdf data")
        file_like.name = "document.pdf"

        self.assertEqual(
            "signed-pdf",
            self.client.sign_pdf(file_like=file_like, reason="approval"),
        )

        self.assertEqual(
            "https://lexwork.example.org/api/signer/v1/pdf_signature_jobs",
            self.requests[0][1],
        )
        self.assertEqual("post", self.requests[0][0])
        self.assertNotIn("data", self.requests[0][2])
        self.assertNotIn("files", self.requests[0][2])
        self.assertEqual(
            {
                "pdf_signature_job": {
                    "file_name": "document.pdf",
                    "data": base64.b64encode(b"pdf data").decode("utf-8"),
                    "reason_for_signature": "approval",
                }
            },
            self.requests[0][2]["json"],
        )

    def test_sign_pdf_payload_is_json_serializable(self):
        file_like = io.BytesIO(b"pdf data")
        file_like.name = "document.pdf"

        self.client.sign_pdf(file_like=file_like, reason="approval")

        json.dumps(self.requests[0][2]["json"])


if __name__ == "__main__":
    unittest.main()
