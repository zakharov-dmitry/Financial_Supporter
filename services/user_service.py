from models import db_session
from models.user import User
from infastructure.hashing import hash_password, verify_password


async def create_new_user(email: str, name: str, password: str):
    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_password(password)
    async with db_session.create_async_session() as session:
        session.add(user)
        await session.commit()
        return user
