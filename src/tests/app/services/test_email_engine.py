import json
import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException
from jinja2 import FileSystemLoader

from app.services.email_engine import EmailService, template_env


class TestEmailEngine(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.original_loader = template_env.loader
        template_env.loader = FileSystemLoader(["tests/templates", "templates"])
        self._original_cache = EmailService._locales_cache.copy()
        EmailService._locales_cache = {
            "es": {"test": "ok_es"},
            "en": {"test": "ok_en"},
        }

    def tearDown(self):
        template_env.loader = self.original_loader
        EmailService._locales_cache = self._original_cache

    def test_get_translation_fallback(self):
        result = EmailService._get_translation_from_cache("en")
        self.assertEqual(result, {"test": "ok_en"})

        result = EmailService._get_translation_from_cache("fr")
        self.assertEqual(result, {"test": "ok_es"})

    def test_render_template(self):
        EmailService._locales_cache["en"] = {
            "test": {"message": "Works!"},
            "base": {
                "subject_prefix": "Test Subject",
                "doubts": "¿Dudas?",
                "contact_text": "Contacta",
                "contact_email": "test@test.com",
                "help_text": "ayuda",
                "thanks": "Gracias",
                "footer_reason": "Razón",
                "rights": "Derechos",
            },
        }

        context = {"key_from_context": "World"}
        translations = EmailService._get_translation_from_cache("en")

        subject, html = EmailService._render_template(
            "test_template/content.html", context, translations
        )

        self.assertEqual(subject, "Test Subject")
        self.assertIn("Hello World", html)
        self.assertIn("Works!", html)

    def test_render_template_not_found(self):
        with self.assertRaises(HTTPException) as cm:
            EmailService._render_template("non_existent_template.html", {}, {})
        self.assertEqual(cm.exception.status_code, 404)

    def test_render_template_fallback_subject(self):
        mock_template = Mock()
        mock_template.blocks = {}
        mock_template.render.return_value = "<html>Content</html>"
        mock_template.new_context.return_value = {}

        translations = {"base": {"subject_prefix": "Fallback Subject"}}

        with patch(
            "app.services.email_engine.template_env.get_template",
            return_value=mock_template,
        ):
            subject, html = EmailService._render_template("any.html", {}, translations)

        self.assertEqual(subject, "Fallback Subject")
        self.assertEqual(html, "<html>Content</html>")

    @patch("app.services.email_engine.resend.Emails.send")
    async def test_send_email_success(self, mock_resend):
        EmailService._locales_cache["es"] = {
            "base": {
                "subject_prefix": "Test",
                "doubts": "?",
                "contact_text": ".",
                "contact_email": "a@b.c",
                "help_text": ".",
                "thanks": ".",
                "footer_reason": ".",
                "rights": ".",
            },
            "test": {"message": "Mock Message"},
        }
        mock_resend.return_value = {"id": "12345"}

        to_email = "test@example.com"
        context = {"key_from_context": "Unit Test"}

        response = await EmailService.send_email(
            to_email, "es", "test_template", context
        )

        mock_resend.assert_called_once()
        call_args = mock_resend.call_args[0][0]
        self.assertEqual(call_args["to"], to_email)
        self.assertIn("Hello Unit Test", call_args["html"])
        self.assertEqual(response, {"id": "12345"})

    @patch("app.services.email_engine.resend.Emails.send")
    async def test_send_email_failure(self, mock_resend):
        EmailService._locales_cache["es"] = {
            "base": {"subject_prefix": "S"},
            "test": {"message": "M"},
        }
        mock_resend.side_effect = Exception("Resend API Down")

        with self.assertRaises(HTTPException) as cm:
            await EmailService.send_email("test@fail.com", "es", "test_template", {})

        self.assertEqual(cm.exception.status_code, 500)
        self.assertIn("Resend API Down", cm.exception.detail)

    @patch("app.services.email_engine.Path")
    def test_load_locales(self, mock_path_cls):
        mock_locales_dir = Mock()
        mock_locales_dir.exists.return_value = True

        mock_file = Mock()
        mock_file.stem = "de"
        mock_file.read_text.return_value = '{"test": "german"}'

        mock_locales_dir.glob.return_value = [mock_file]

        # Mock the chain Path(__file__).parent.parent / "locales"
        mock_path_cls.return_value.parent.parent.__truediv__.return_value = (
            mock_locales_dir
        )

        EmailService._locales_cache = {}
        EmailService.load_locales()

        self.assertIn("de", EmailService._locales_cache)
        self.assertEqual(EmailService._locales_cache["de"], {"test": "german"})

    @patch("app.services.email_engine.Path")
    def test_load_locales_directory_not_found(self, mock_path_cls):
        mock_locales_dir = Mock()
        mock_locales_dir.exists.return_value = False

        mock_path_cls.return_value.parent.parent.__truediv__.return_value = (
            mock_locales_dir
        )

        EmailService._locales_cache = {}
        EmailService.load_locales()

        self.assertEqual(EmailService._locales_cache, {})

    @patch("app.services.email_engine.Path")
    def test_load_locales_json_error(self, mock_path_cls):
        mock_locales_dir = Mock()
        mock_locales_dir.exists.return_value = True

        mock_file_ok = Mock()
        mock_file_ok.stem = "ok"
        mock_file_ok.read_text.return_value = "{}"

        mock_file_bad = Mock()
        mock_file_bad.name = "bad.json"
        mock_file_bad.read_text.side_effect = json.JSONDecodeError("Fail", "doc", 0)

        mock_locales_dir.glob.return_value = [mock_file_ok, mock_file_bad]
        mock_path_cls.return_value.parent.parent.__truediv__.return_value = (
            mock_locales_dir
        )

        EmailService._locales_cache = {}
        EmailService.load_locales()

        self.assertIn("ok", EmailService._locales_cache)

    @patch("app.services.email_engine.Path")
    def test_load_locales_generic_exception(self, mock_path_cls):
        mock_path_cls.side_effect = Exception("Catastrophic filesystem failure")

        EmailService.load_locales()
