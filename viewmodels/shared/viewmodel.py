from typing import Optional
from fastapi import Request

from infastructure.security import get_current_user_from_cookies


class ViewModelBase:

    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.current_user: Optional[str] = get_current_user_from_cookies(request)
        self.is_logged_in: bool = self.current_user is not None

    def to_dict(self) -> dict:
        return self.__dict__
