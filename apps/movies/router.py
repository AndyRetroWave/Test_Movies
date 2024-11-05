from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer

from apps.auth.services_auth import GetTokenType
from apps.movies.services import MovieServices
from apps.user.models import User


movie_services = MovieServices()

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/movies",
    tags=["Фильмы"],
    dependencies=[Depends(http_bearer)],
)


@router.get("/search", dependencies=[Depends(GetTokenType.get_current_auth_user)])
async def search_movies(query: str = Query(..., description="Название фильма")):
    """Получение списков фильмов по названию"""
    return await movie_services.get_movies_search(query)


@router.get(
    "/{kinopoisk_id}", dependencies=[Depends(GetTokenType.get_current_auth_user)]
)
async def get_movies_detail(kinopoisk_id: int):
    """Получение информации о фильме по ID"""
    return await movie_services.get_detail_movie(kinopoisk_id)


@router.post("/favorites")
async def add_favorite_movies_user(
    id: int = Query(..., description="ID фильма"),
    current_user: User = Depends(GetTokenType.get_current_auth_user),
):
    """Добавление фильма в список любимых"""
    result = await movie_services.add_favorite_movies_user_services(
        id, int(current_user.id)
    )
    if result:
        return {"message": "Фильм успешно добавлен в ваши любимые фильмы"}


@router.delete("/favorites/{kinopoisk_id}")
async def delete_favorites_id(
    kinopoisk_id: int, current_user: User = Depends(GetTokenType.get_current_auth_user)
):
    """Удаление фильма из списка любимых"""
    result: bool = await movie_services.delete_favorite_movies_user_services(
        kinopoisk_id, int(current_user.id)
    )
    if result:
        return {"message": "Фильм удален из списка любимых"}


@router.get("/movies/favorites")
async def get_favorite_movies(
    current_user: User = Depends(GetTokenType.get_current_auth_user),
):
    """Получение списка любимых фильмов"""
    result = await movie_services.get_favorite_movies_services(current_user.id)
    return result
