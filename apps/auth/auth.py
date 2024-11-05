from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from apps.auth.services_auth import TokenAuthValidate
from apps.user.shemas import UserRegister, UserShemas

from .jwt import (
    CreateTokenPayload,
    TokenInfo,
)
from .services_auth import AuthServices, GetTokenType

auth_app = FastAPI()

http_bearer = HTTPBearer(auto_error=False)
auth_services = AuthServices()

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register")
async def post_register(
    user: UserRegister,
):
    result_user_register: bool = await auth_services.add_register_user(user)
    if result_user_register:
        return HTTPException(
            status_code=HTTP_200_OK, detail="Пользователь зарегестрирован!"
        )


@router.post("/login")
async def post_login(
    user: UserShemas = Depends(TokenAuthValidate.validate_user_login),
) -> TokenInfo:
    result: TokenInfo = await auth_services.validate_login(user)
    if result:
        return result
    return HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Ошибка авторизации")


@router.get("/profil")
async def check_email(
    current_user: UserShemas = Depends(GetTokenType.get_current_auth_user),
) -> UserRegister:
    return UserRegister(
        given_name=current_user.given_name,
        family_name=current_user.family_name,
        email=current_user.email,
        password="Пароль захеширован",
    )


@router.post("/refresh", response_model=TokenInfo)
async def auth_refresh_token(
    user: UserShemas = Depends(GetTokenType.get_current_auth_refresh_token),
):
    """Для того чтобы обновить access токен нужно в HTTPBearer вставить refresh токен,\
после чего он обновиться, по хорошему его надо сохранять в базу данных, но не стал этого делать для упрощения"""
    access_token: str = await CreateTokenPayload.create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )
