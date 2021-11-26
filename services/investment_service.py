import datetime

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


async def add_investment_for_user(
        title: str,
        code: str,
        amount: int,
        purchase_date: datetime.date,
        avg_prise: float,
        purchase_prise: int,
        closing_date: datetime.date,
        owner_email: str,
        value: int = None
        ):
    investment = Investment()
    investment.title = title
    investment.code = code
    investment.amount = amount
    investment.value = value
    investment.purchase_date = purchase_date
    investment.avg_prise = avg_prise
    investment.purchase_prise = purchase_prise
    investment.closing_date = closing_date
    investment.owner_email = owner_email
    async with db_session.create_async_session() as session:
        session.add(investment)
        await session.commit()

        return investment


