from typing import List, Optional
from fastapi import Request

from services.investment_service import all_investments_for_user
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.user: str = "DmitryZ"
        self.investments: Optional[List] = all_investments_for_user()
