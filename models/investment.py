from sqlalchemy import ForeignKey
import sqlalchemy as sa
import sqlalchemy.orm as orm

from models.modelbase import SqlAlchemyBase


class Investment(SqlAlchemyBase):
    __tablename__ = 'investments'
    title: str = sa.Column(sa.String, nullable=False, index=True)
    id: str = sa.Column(sa.String, primary_key=True)
    amount: int = sa.Column(sa.Integer, nullable=False)
    coupon: float = sa.Column(sa.Float, nullable=False)
    owner_email: str = sa.Column(sa.String, ForeignKey('users.email'))
    owner = sa.orm.relationship("User", back_populates="investments")


