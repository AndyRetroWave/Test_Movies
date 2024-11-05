from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jwt import InvalidTokenError

from apps.auth.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    CreateTokenPayload,
    TokenInfo,
)
from apps.auth.password import check_password, hash_password
from apps.user.dao import UserDAO
from apps.user.models import User
from apps.user.shemas import UserRegister, UserShemas

http_bearer = HTTPBearer()


class TokenAuthValidate:
    @staticmethod
    async def validate_user_login(email: str, password: str) -> User:
        user: User = await UserDAO.get_user_by_email(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        valid_pass: bool = await check_password(password, user.hashed_password)
        if not valid_pass:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
            )
        if user.is_active:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не активен!"
        )

    @staticmethod
    async def get_current_token_payload(
        credentials: HTTPBasicCredentials = Depends(http_bearer),
    ) -> UserShemas:
        if isinstance(credentials, str):
            token: str = credentials
        else:
            token: str = credentials.credentials
        if token is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Отстуствует токен"
            )
        try:
            payload: dict = await CreateTokenPayload.decode_jwt(token=token)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
            )
        return payload  # type: ignore

    @staticmethod
    async def get_current_auth_data(
        type_token: str,
        payload: dict = Depends(get_current_token_payload),
    ) -> UserShemas:
        token_type: str | None = payload.get(TOKEN_TYPE_FIELD)  # type: ignore
        if token_type != type_token:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Вы указали не верный тип токена, укажите access_token!",
            )
        email: str | None = payload.get("sub")  # type: ignore
        user_data: User | None = await UserDAO.get_user_by_email(email=email)  # type: ignore
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user_data  # type: ignore


class GetTokenType:
    token = TokenAuthValidate

    @staticmethod
    async def get_current_auth_user(
        payload: dict = Depends(token.get_current_token_payload),
    ) -> UserShemas:
        return await TokenAuthValidate.get_current_auth_data(
            type_token=ACCESS_TOKEN_TYPE, payload=payload
        )

    @staticmethod
    async def get_current_auth_refresh_token(
        payload: dict = Depends(token.get_current_token_payload),
    ) -> UserShemas:
        return await TokenAuthValidate.get_current_auth_data(
            type_token=REFRESH_TOKEN_TYPE, payload=payload
        )

    @staticmethod
    async def get_current_active_auth_user(
        user: UserShemas = Depends(get_current_auth_user),
    ) -> UserShemas:
        user_data: User | None = await UserDAO.get_user_by_email(email=user.email)
        if user_data is None or not user_data.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не активен!",
            )
        return user_data  # type: ignore


class AuthServices:
    dao = UserDAO()

    async def add_register_user(self, user: UserRegister) -> UserShemas | bool:
        hashed_password = await hash_password(user.password)
        await self.dao.add_user(
            user.given_name, user.family_name, user.email, hashed_password
        )
        return True

    async def validate_login(
        self, user: UserShemas = Depends(TokenAuthValidate.validate_user_login)
    ) -> TokenInfo | bool:
        try:
            access_token: str = await CreateTokenPayload.create_access_token(user)
            refresh_token: str = await CreateTokenPayload.create_refresh_token(user)
            return TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except Exception:
            return False
