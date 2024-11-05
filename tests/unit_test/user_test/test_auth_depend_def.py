import pytest

from apps.auth.jwt import CreateTokenPayload
from apps.auth.services_auth import GetTokenType, TokenAuthValidate
from tests.integtation_test.test_auth_api import FAKE


@pytest.mark.asycio
@pytest.mark.parametrize(
    ("email", "password", "test_email"),
    [("john.doe@example.com", "Andreykiller566576!", "john.doe@example.com")],
)
async def test_validate_user_login(email: str, password: str, test_email):
    result = await TokenAuthValidate.validate_user_login(email, password)
    assert result.email == test_email


@pytest.mark.asyncio
async def test_get_current_token_payload():
    access_token = await CreateTokenPayload.encode_jwt(
        payload={
            "sub": "john.doe@example.com",
            "type": "access_token",
            "given_name": FAKE.first_name_male(),
            "family_name": FAKE.last_name_male(),
            "iat": FAKE.date_time(),
        }
    )
    payload = await CreateTokenPayload.decode_jwt(token=access_token)
    payload_result = await TokenAuthValidate.get_current_token_payload(access_token)
    await GetTokenType.get_current_auth_user(payload_result)
    assert payload_result == payload
