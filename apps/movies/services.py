import httpx
from fastapi import HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from apps.config import settings
from apps.movies.dao import UserFavoriteDao


async def get_url_httpx_search(url):
    async with httpx.AsyncClient() as client:
        headers = {
            "X-API-KEY": f"{settings.API_KEY_KINOPOISK}",
            "Content-Type": "application/json",
        }
        response = await client.get(
            url=url,
            headers=headers,
        )
        if response.status_code == 200:
            response.raise_for_status()
            return response.json()
        elif response.status_code == 401:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
        elif response.status_code == 402:
            raise HTTPException(status_code=HTTP_402_PAYMENT_REQUIRED)
        elif response.status_code == 404:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Фильм не найден!"
            )


class MovieServices:
    dao = UserFavoriteDao()

    async def get_movies_search(self, query: str):
        data = await get_url_httpx_search(
            f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={query}"
        )
        return data

    async def get_detail_movie(self, id: int):
        data = await get_url_httpx_search(
            f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}"
        )
        return data

    async def add_favorite_movies_user_services(self, id: int, user_id: int):
        data = await self.get_detail_movie(id)
        await self.dao.add_movies_favorite_user(id, user_id, data)
        return True

    async def delete_favorite_movies_user_services(self, id: int, user_id: int):
        result: bool = await self.dao.delete_movies_favorite_user(id, user_id)
        if result:
            return True
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Фильм не найден в списке любимых!"
        )

    async def get_favorite_movies_services(self, id_user: int):
        try:
            result = await self.dao.get_favorite_movies_all(id_user)
            if result == []:
                return HTTPException(status_code=HTTP_200_OK, detail="Вас список пуст")
            if result:
                return result
        except Exception:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )
