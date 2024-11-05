from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_400_BAD_REQUEST

from apps.base_dao import BaseDAO
from apps.database import async_session_maker
from apps.user.models import User


class UserDAO(BaseDAO):
    model = User  # type: ignore

    @classmethod
    async def add_user(
        cls,
        given_names: str,
        family_names: str,
        email: str,
        password: str,
    ):
        try:
            async with async_session_maker() as session:
                user = insert(cls.model).values(
                    given_name=given_names,
                    family_name=family_names,
                    email=email,
                    hashed_password=password,
                )
                await session.execute(user)
                await session.commit()
                return user
        except SQLAlchemyError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Такой пользователь уже зарегестрирован",
            )

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.email == email)  # type: ignore
            result = await session.execute(query)
            return result.scalar_one_or_none()
