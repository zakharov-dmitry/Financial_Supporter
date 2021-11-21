from sqlalchemy.future import select
import sqlalchemy.orm

from models import db_session
from models.investment import Investment


async def all_investments_for_user():
    async with db_session.create_async_session() as session:
        query = select(Investment) \
            .options(sqlalchemy.orm.joinedload(Investment.owner)) \
            .order_by(Investment.amount.desc())
        result = await session.execute(query)
        investments = result.scalars()
        return investments


async def add_investment_for_user(title: str, id: str, amount: int, coupon: float, owner_email: str):
    investment = Investment()
    investment.title = title
    investment.id = id
    investment.amount = amount
    investment.coupon = coupon
    investment.owner_email = owner_email
    async with db_session.create_async_session() as session:
        session.add(investment)
        await session.commit()

        return investment


