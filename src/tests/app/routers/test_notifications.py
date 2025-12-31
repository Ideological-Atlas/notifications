import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.config import settings
from main import app


class TestNotificationsRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.url = "/notifications/send"
        self.valid_headers = {"x-api-key": settings.API_KEY}
        self.valid_payload = {
            "to_email": "user@example.com",
            "template_name": "test_template",
            "language": "es",
            "context": {"name": "User"},
        }

    def test_send_notification_unauthorized(self):
        headers = {"x-api-key": "wrong-key"}
        response = self.client.post(self.url, json=self.valid_payload, headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Invalid Authentication Credentials"
        )

    def test_send_notification_bad_request(self):
        invalid_payload = {"template_name": "missing_email"}
        response = self.client.post(
            self.url, json=invalid_payload, headers=self.valid_headers
        )
        self.assertEqual(response.status_code, 422)

    @patch("app.services.email_engine.EmailService.send_email", new_callable=AsyncMock)
    def test_send_notification_success(self, mock_send_email):
        mock_send_email.return_value = {"id": "resend_id_123"}

        response = self.client.post(
            self.url, json=self.valid_payload, headers=self.valid_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "success", "provider_response": {"id": "resend_id_123"}},
        )

        mock_send_email.assert_awaited_once_with(
            to_email="user@example.com",
            language="es",
            template_name="test_template",
            context={"name": "User"},
        )
