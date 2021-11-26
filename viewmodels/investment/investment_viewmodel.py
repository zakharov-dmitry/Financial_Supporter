from datetime import datetime

from fastapi import Request, HTTPException

from infastructure.num_convert import try_int, try_float
from infastructure.security import validate_current_user_from_token
from models.user import User
from viewmodels.shared.viewmodel import ViewModelBase


class InvestmentViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.title: str = None
        self.code: str = None
        self.amount: int = None
        self.value: int = None
        self.owner: User = None
        self.purchase_date: datetime.date = None
        self.avg_prise: float = None
        self.purchase_prise: int = None
        self.closing_date: datetime.date = None

    async def load(self):
        form = await self.request.form()
        self.title = form.get('title')
        self.code = form.get('code')
        self.amount = try_int(form.get('amount'))
        self.value = try_int(form.get('value'))
        self.purchase_date = datetime.strptime(form.get('purchase_date'), "%Y-%m-%d")
        self.avg_prise = try_float(form.get('avg_prise'))
        self.purchase_prise = try_int(form.get('purchase_prise'))
        self.closing_date = datetime.strptime(form.get('closing_date'), "%Y-%m-%d")
        if not self.title:
            self.error = "Title is missing"
        elif not self.code:
            self.error = "Code is missing"
        elif not self.amount or self.amount <= 0:
            self.error = "Amount must be greater than 0"
        elif not self.purchase_date:
            self.error = "Purchase date is missing"
        elif not self.purchase_prise:
            self.error = "Purchase prise is missing"
        elif not self.closing_date:
            self.error = "Closing date is missing"
        else:
            try:
                self.owner = await validate_current_user_from_token(self.request)
            except HTTPException as Error:
                self.error = Error.detail
