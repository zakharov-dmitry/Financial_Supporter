from fastapi import Request, HTTPException

from infastructure.security import validate_current_user_from_token
from models.user import User
from viewmodels.shared.viewmodel import ViewModelBase


class InvestmentViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.title: str = None
        self.id: str = None
        self.amount: int = None
        self.coupon: float = None
        self.owner: User = None

    async def load(self):
        form = await self.request.form()
        self.title = form.get('title')
        self.id = form.get('id')
        self.amount = int(form.get('amount'))
        self.coupon = float(form.get('coupon'))
        if not self.title:
            self.error = "Title is missing"
        elif not self.id:
            self.error = "ID is missing"
        elif not self.amount or self.amount <= 0:
            self.error = "Amount must be greater than 0"
        elif not self.coupon or self.coupon <= 0:
            self.error = "Coupon must be greater than 0"
        else:
            try:
                self.owner = await validate_current_user_from_token(self.request)
            except HTTPException as Error:
                self.error = Error.detail
