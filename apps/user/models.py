from sqlalchemy import Boolean, Column, Integer, String

from apps.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    given_name = Column(String, nullable=True, index=True)
    family_name = Column(String, nullable=True, index=True, default=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
