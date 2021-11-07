from models.modelbase import SqlAlchemyBase
import sqlalchemy as sa


class Investment(SqlAlchemyBase):
    __tablename__ = 'investments'
    title: str = sa.Column(sa.String, nullable=False, index=True)
    id: str = sa.Column(sa.String, primary_key=True)
    amount: int = sa.Column(sa.Integer, nullable=False)
    coupon: int = sa.Column(sa.Float, nullable=False)
