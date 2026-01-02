import unittest

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import api_key_auth


class TestSecurity(unittest.IsolatedAsyncioTestCase):

    async def test_api_key_auth_valid(self):
        header_value = f"Bearer {settings.API_KEY}"
        result = await api_key_auth(auth_value=header_value)
        self.assertEqual(result, settings.API_KEY)

    async def test_api_key_auth_invalid_key(self):
        header_value = "Bearer wrong-key"
        with self.assertRaises(HTTPException) as cm:
            await api_key_auth(auth_value=header_value)

        self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(cm.exception.detail, "Invalid Credentials")

    async def test_api_key_auth_invalid_scheme(self):
        header_value = settings.API_KEY
        with self.assertRaises(HTTPException) as cm:
            await api_key_auth(auth_value=header_value)

        self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
