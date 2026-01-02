from fastapi import APIRouter, Depends

from app.core.security import api_key_auth
from app.schemas.email import EmailRequest
from app.services.email_engine import EmailService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/send")
async def send_notification(email_data: EmailRequest, _: str = Depends(api_key_auth)):
    result = await EmailService.send_email(
        to_email=email_data.to_email,
        language=email_data.language,
        template_name=email_data.template_name,
        context=email_data.context,
    )

    return {"status": "success", "provider_response": result}
