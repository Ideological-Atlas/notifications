import json
import logging
from datetime import datetime
from pathlib import Path

import resend
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from app.core.config import settings
from app.core.theme import theme

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY
template_env = Environment(
    loader=FileSystemLoader(settings.TEMPLATE_FOLDER), autoescape=True
)


class EmailService:
    _locales_cache: dict[str, dict] = {}

    @classmethod
    def load_locales(cls) -> None:
        try:
            locales_dir = Path(__file__).parent.parent / "locales"
            if not locales_dir.exists():
                logger.warning("Locales directory not found: %s", locales_dir)
                return

            for file_path in locales_dir.glob("*.json"):
                try:
                    content = json.loads(file_path.read_text(encoding="utf-8"))
                    cls._locales_cache[file_path.stem] = content
                    logger.info("Loaded locale: %s", file_path.stem)
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON for locale: %s", file_path.name)
        except Exception as e:
            logger.error("Error loading locales: %s", e)

    @classmethod
    def _get_translation_from_cache(cls, language: str) -> dict:
        if language not in cls._locales_cache:
            logger.warning(
                "Language '%s' not found in cache, falling back to 'es'", language
            )
            return cls._locales_cache.get("es", {})
        return cls._locales_cache[language]

    @staticmethod
    def _render_template(
        template_path: str, specific_context: dict, translations: dict
    ) -> tuple[str, str]:
        logger.debug("Rendering template: %s", template_path)

        global_context = {
            "site_url": settings.BASE_SITE_URL,
            "project_name": settings.PROJECT_NAME,
            "t": translations,
            "year": datetime.now().year,
            "theme": theme,
        }
        final_context = {**global_context, **specific_context}

        try:
            template = template_env.get_template(template_path)
        except TemplateNotFound:
            logger.error("Template NOT FOUND at path: %s", template_path)
            raise HTTPException(
                status_code=404, detail=f"Template not found: {template_path}"
            )

        html_content = template.render(final_context)

        try:
            subject_block = template.blocks["subject"]
            ctx = template.new_context(final_context)
            subject = "".join(subject_block(ctx))
        except KeyError:
            logger.warning(
                "Could not find subject block for template: %s", template_path
            )
            subject = translations.get("base", {}).get("subject_prefix", "Notification")

        return subject, html_content

    @classmethod
    async def send_email(
        cls, to_email: str, language: str, template_name: str, context: dict
    ):
        template_path = f"{template_name}/content.html"

        translations = cls._get_translation_from_cache(language)

        logger.info(
            "Processing email request -> To: %s | Template: %s | Lang: %s",
            to_email,
            template_path,
            language,
        )

        subject, html_content = cls._render_template(
            template_path, context, translations
        )

        from_address = f"{settings.FROM_EMAIL_NAME} <{settings.FROM_EMAIL}>"

        try:
            logger.debug("Sending via Resend API to %s...", to_email)

            response = resend.Emails.send(
                {
                    "from": from_address,
                    "to": to_email,
                    "subject": subject,
                    "html": html_content,
                }
            )

            logger.info(
                "Email sent successfully to %s. Resend ID: %s",
                to_email,
                response.get("id", "unknown"),
            )
            return response

        except Exception as e:
            logger.error(
                "Failed to send email via Resend to %s. Error: %s",
                to_email,
                str(e),
                exc_info=True,
            )
            raise HTTPException(status_code=500, detail=str(e))
