import re
from fastapi import status, HTTPException
import bcrypt


async def hash_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?])(?=.{8,})'
    if re.match(pattern, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        hashed_password_str = hashed_password.decode("utf-8")
        return hashed_password_str
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid password")


async def check_password(password, hashed_password):
    check_password = bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )
    if check_password:
        return True
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid password")
