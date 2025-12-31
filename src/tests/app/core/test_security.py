import unittest

from fastapi import HTTPException

from app.core.config import settings
from app.core.security import verify_api_key


class TestSecurity(unittest.IsolatedAsyncioTestCase):

    async def test_verify_api_key_valid(self):
        result = await verify_api_key(x_api_key=settings.API_KEY)
        self.assertEqual(result, settings.API_KEY)

    async def test_verify_api_key_invalid(self):
        with self.assertRaises(HTTPException) as cm:
            await verify_api_key(x_api_key="wrong-key")

        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.detail, "Invalid Authentication Credentials")
