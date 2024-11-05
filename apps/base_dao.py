from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from apps.database import async_session_maker
from apps.logger import logger


def session_handler_exceptions(func):
    async def wrapper(self, *args, **kwargs):
        try:
            async with async_session_maker() as session:
                result = await func(self, session, *args, **kwargs)
                await session.commit()
                return result
        except IntegrityError as e:
            logger.error("Ошибка целостности: %s", e.orig)
            await session.rollback()
            raise IndentationError()
        except OperationalError as e:
            logger.error("Эксплуатационная ошибка: %s", e.orig)
            raise OperationalError()
        except SQLAlchemyError as e:
            logger.error("Произошла ошибка базы: %s", e.args)
            raise SQLAlchemyError()
        except Exception as e:
            logger.error("Произошла неизвестная ошибка в базе: %s", e)
            raise Exception()

    return wrapper


class BaseDAO:
    model = None

    @session_handler_exceptions
    async def find_by_id(self, session, model_id: int):
        query = select(self.model).filter_by(id=model_id)  # type: ignore
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @session_handler_exceptions
    async def find_one_or_none(self, session, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @session_handler_exceptions
    async def find_scalar(self, session, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar()

    @session_handler_exceptions
    async def get_all(self, session, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars()

    @session_handler_exceptions
    async def add(self, session, **data):
        query = insert(self.model).values(**data)
        await session.execute(query)
