from sqlalchemy import delete, insert, select

from apps.base_dao import BaseDAO, session_handler_exceptions
from apps.movies.model import UserMoviesFavorite


class UserFavoriteDao(BaseDAO):
    model = UserMoviesFavorite  # type: ignore

    @session_handler_exceptions
    async def add_movies_favorite_user(
        self, session, id_movies_favorite: str, user: str, data: dict
    ):
        user = insert(self.model).values(
            id_movies_favorite=id_movies_favorite, id_user=user, data_movies=data
        )
        await session.execute(user)

    @session_handler_exceptions
    async def get_user_by_email(self, session, email: str):
        query = select(self.model).where(self.model.email == email)  # type: ignore
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @session_handler_exceptions
    async def delete_movies_favorite_user(
        self, session, id_movies_favorite: int, user_id: int
    ):
        search_data = await session.execute(
            select(self.model).filter(
                self.model.id_user == user_id,
                self.model.id_movies_favorite == id_movies_favorite,
            )
        )
        if search_data.scalar() is None:
            return False
        await session.execute(
            delete(self.model).filter(
                self.model.id_user == user_id,
                self.model.id_movies_favorite == id_movies_favorite,
            )
        )
        return True

    @session_handler_exceptions
    async def get_favorite_movies_all(self, session, id_user: int):
        smtp = await session.execute(
            select(self.model.data_movies).filter(self.model.id_user == id_user)
        )
        return smtp.scalars().all()
