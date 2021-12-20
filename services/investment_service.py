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


def get_coupons_for_investment(code: str):
    data = {"RU000A100D89": {"2020-11-05": 42.38,
                             "2021-05-06": 42.38,
                             "2021-11-04": 42.38,
                             "2022-05-05": 42.38,
                             "2022-11-03": 42.38,
                             "2023-05-04": 42.38,
                             "2023-11-02": 42.38,
                             "2024-05-02": 42.38,
                             "2024-10-31": 42.38,
                             "2025-05-01": 42.38},
            "RU000A100YP2": {"2020-01-23": 33.66,
                             "2020-04-23": 33.66,
                             "2020-07-23": 33.66,
                             "2020-10-22": 33.66,
                             "2021-01-21": 33.66,
                             "2021-04-22": 33.66,
                             "2021-07-22": 33.66,
                             "2021-10-21": 33.66,
                             "2022-01-22": 33.66,
                             "2022-04-21": 33.66,
                             "2022-07-21": 33.66,
                             "2022-10-20": 33.66},
            "RU000A100Q35": {"2019-09-12": 9.86,
                             "2019-10-14": 9.86,
                             "2019-11-11": 9.86,
                             "2019-12-11": 9.86,
                             "2020-01-10": 9.86,
                             "2020-02-10": 9.86,
                             "2020-03-10": 9.86,
                             "2020-04-09": 9.86,
                             "2020-05-12": 9.86,
                             "2020-06-08": 9.86,
                             "2020-07-08": 9.86,
                             "2020-08-07": 9.86,
                             "2020-09-07": 9.86,
                             "2020-10-06": 9.86,
                             "2020-11-05": 9.86,
                             "2020-12-07": 9.86,
                             "2021-01-11": 9.86,
                             "2021-02-03": 9.86,
                             "2021-03-05": 9.86,
                             "2021-04-05": 9.86,
                             "2021-05-04": 9.86,
                             "2021-06-03": 9.86,
                             "2021-07-05": 9.86,
                             "2021-08-02": 9.86,
                             "2021-09-01": 9.86,
                             "2021-10-01": 9.86,
                             "2021-10-31": 9.86,
                             "2021-11-30": 9.86,
                             "2021-12-30": 9.86,
                             "2022-01-29": 9.86,
                             "2022-02-28": 8.22,
                             "2022-03-30": 8.22,
                             "2022-04-29": 8.22,
                             "2022-05-29": 8.22,
                             "2022-06-28": 8.22,
                             "2022-07-28": 8.22,
                             "2022-08-27": 8.22,
                             "2022-09-26": 8.22,
                             "2022-10-26": 8.22,
                             "2022-11-25": 8.22,
                             "2022-12-25": 8.22,
                             "2023-01-24": 8.22,
                             "2023-02-23": 8.22,
                             "2023-03-25": 8.22,
                             "2023-04-24": 8.22,
                             "2023-05-24": 8.22,
                             "2023-06-23": 8.22,
                             "2023-07-23": 8.22,
                             "2023-08-22": 8.22,
                             "2023-09-21": 8.22,
                             "2023-10-21": 8.22,
                             "2023-11-20": 8.22,
                             "2023-12-20": 8.22,
                             "2024-01-19": 8.22,
                             "2024-02-18": 8.22,
                             "2024-03-19": 8.22,
                             "2024-04-18": 8.22,
                             "2024-05-18": 8.22,
                             "2024-06-17": 8.22,
                             "2024-07-17": 8.22,
                             "2024-08-16": 8.22,
                             "2024-09-15": 8.22,
                             "2024-10-15": 8.22,
                             "2024-11-14": 8.22,
                             "2024-12-14": 8.22,
                             "2025-01-13": 8.22,
                             "2025-02-12": 8.22,
                             "2025-03-14": 8.22,
                             "2025-04-13": 8.22,
                             "2025-05-13": 8.22,
                             "2025-06-12": 8.22,
                             "2025-07-12": 8.22,
                             "2025-08-11": 8.22,
                             "2025-09-10": 8.22,
                             "2025-10-10": 8.22,
                             "2025-11-09": 8.22,
                             "2025-12-09": 8.22,
                             "2026-01-08": 8.22,
                             "2026-02-07": 8.22,
                             "2026-03-09": 8.22,
                             "2026-04-08": 8.22,
                             "2026-05-08": 8.22,
                             "2026-06-07": 8.22,
                             "2026-07-07": 8.22,}
            }
    return data[code]


def get_prise_for_investment(code: str):
    data = {"RU000A100D89": 92.06,
            "RU000A100YP2": 99.27,
            "RU000A100Q35": 100.1}
    return data[code]
