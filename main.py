import logging

import uvicorn
from fastapi import FastAPI

from apps.auth.auth import auth_app
from apps.auth.auth import router as router_users
from apps.movies.router import router as router_movies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


app.include_router(router_users)
app.include_router(router_movies)

app.mount("/", auth_app)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
