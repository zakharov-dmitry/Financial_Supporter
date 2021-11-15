from typing import List, Optional
from fastapi import Request

from services.investment_service import all_investments_for_user
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.admin: str = "Dmitry_Zakharov"
        self.investments: Optional[List] = None

    async def load(self):
        self.investments: Optional[List] = await all_investments_for_user()

