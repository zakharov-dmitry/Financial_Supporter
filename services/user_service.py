from typing import Optional

from sqlalchemy.future import select

from models import db_session
from models.user import User
from infastructure.hashing import hash_password, verify_password


async def create_new_user(email: str, name: str, password: str) -> Optional[User]:
    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_password(password)
    async with db_session.create_async_session() as session:
        session.add(user)
        await session.commit()
        return user


async def get_user_by_email(email: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if not user:
        return None
    elif not verify_password(password, user.hashed_password):
        return None
    return user