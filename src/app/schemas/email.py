from typing import Any

from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    to_email: EmailStr
    template_name: str
    language: str = "es"
    context: dict[str, Any] = {}
