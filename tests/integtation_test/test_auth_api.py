import pytest
from faker import Faker
from httpx import AsyncClient

from main import app

FAKE = Faker()


@pytest.fixture
async def ac():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("john.doe@example.com", "Andreykiller566576!", 200),
        ("jane.smith@example.com", "Andreykiller566576", 401),
        ("vasia.johnson@example.co.m", "Andreykiller566576!", 401),
    ],
)
async def test_login_api(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", data={"email": email, "password": password})
    assert response.status_code == status_code
    if status_code == 200:
        json_response = response.json()
        access_token = json_response["access_token"]
        protected_response = await ac.get(
            "/auth/profil",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert protected_response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("given_name", "family_name", "email", "password", "status_code"),
    [
        (
            FAKE.first_name_male(),
            FAKE.last_name_male(),
            FAKE.email(),
            FAKE.password(length=5),
            401,
        ),
        (
            FAKE.first_name_male(),
            FAKE.last_name_male(),
            FAKE.email(),
            FAKE.password(length=15, special_chars=True, upper_case=True),
            200,
        ),
    ],
)
async def test_register_api(
    given_name: str,
    family_name: str,
    email: str,
    password: str,
    status_code: int,
    ac: AsyncClient,
):
    response = await ac.post(
        "/auth/register",
        data={
            "given_name": given_name,
            "family_name": family_name,
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
