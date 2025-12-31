import os
import unittest
from importlib import reload
from unittest.mock import patch

from app.core import config


class TestConfig(unittest.TestCase):
    def test_settings_load_correctly(self):
        dummy_required_env = {
            "RESEND_API_KEY": "mock_resend_key",
            "API_KEY": "mock_api_key",
            "FROM_EMAIL": "no-reply@test.com",
            "FROM_EMAIL_NAME": "Test Sender",
            "BASE_BACKEND_URL": "http://localhost:8000",
        }
        with patch.dict(os.environ, dummy_required_env, clear=True):
            reload(config)
            self.assertEqual(config.settings.PROJECT_NAME, "Email Service")
            self.assertEqual(config.settings.TEMPLATE_FOLDER, "templates")

    @patch.dict(os.environ, {"PROJECT_NAME": "Test Project", "LOG_LEVEL": "DEBUG"})
    def test_settings_override_from_env(self):
        reload(config)
        self.assertEqual(config.settings.PROJECT_NAME, "Test Project")
        self.assertEqual(config.settings.LOG_LEVEL, "DEBUG")
