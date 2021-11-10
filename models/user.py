import datetime
from typing import Optional

from models.modelbase import SqlAlchemyBase
import sqlalchemy as sa


# def set_default_name(context):
#     return context.get_current_parameters()['email']

class User(SqlAlchemyBase):
    __tablename__ = "users"
    id: int = sa.Column(sa.Integer, index=True, autoincrement=True)
    email: str = sa.Column(sa.String, primary_key=True)
    name: Optional[str] = sa.Column(sa.String, default=email)
    hashed_password: str = sa.Column(sa.String, nullable=False)
    is_active: bool = sa.Column(sa.Boolean, default=True)
    create_date: datetime = sa.Column(sa.DateTime, default=datetime.datetime.now())
