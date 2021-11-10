import datetime
from typing import Optional, List

from models.investment import Investment
from models.modelbase import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm


def set_default_name(context):
    return context.get_current_parameters()['email']


class User(SqlAlchemyBase):
    __tablename__ = "users"
    email: str = sa.Column(sa.String, primary_key=True)
    name: Optional[str] = sa.Column(sa.String, default=set_default_name)
    hashed_password: str = sa.Column(sa.String, nullable=False)
    is_active: bool = sa.Column(sa.Boolean, default=True)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now)
    investments: List[Investment] = orm.relationship("Investment", back_populates='owner')