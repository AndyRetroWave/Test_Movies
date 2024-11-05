from sqlalchemy import JSON, Column, ForeignKey, Integer

from apps.database import Base


class UserMoviesFavorite(Base):
    __tablename__ = "favorite_movies"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    id_movies_favorite = Column(Integer, nullable=True, index=True, default=True)
    data_movies = Column(JSON, nullable=True)

    async def __repr__(self):
        return (
            f"<UserMoviesFavorite(id={self.id}, id_user={self.id_user}",
            f"<id_movies_favorite={self.id_movies_favorite}, data_movies={self.data_movies}>",
        )

    async def __str__(self):
        return (
            f"<UserMoviesFavorite(id={self.id}, id_user={self.id_user}",
            f"<id_movies_favorite={self.id_movies_favorite}, data_movies={self.data_movies}>",
        )
