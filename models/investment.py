from datetime import datetime

from sqlalchemy import ForeignKey
import sqlalchemy as sa
import sqlalchemy.orm as orm

from models.modelbase import SqlAlchemyBase


class Investment(SqlAlchemyBase):
    __tablename__ = 'investments'
    id: int = sa.Column(sa.Integer, primary_key=True)
    code: str = sa.Column(sa.String, nullable=False, index=True)
    title: str = sa.Column(sa.String, nullable=False)
    value: int = sa.Column(sa.Integer, default=1000)
    amount: int = sa.Column(sa.Integer, nullable=False)
    purchase_date: datetime.date = sa.Column(sa.Date, nullable=False)
    purchase_prise: int = sa.Column(sa.Integer, nullable=False)
    closing_date: datetime.date = sa.Column(sa.Date, nullable=False)
    owner_email: str = sa.Column(sa.String, ForeignKey('users.email'))
    owner = sa.orm.relationship("User", back_populates="investments")


