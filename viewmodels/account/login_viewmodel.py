from fastapi import Request

from services import user_service
from viewmodels.shared.viewmodel import ViewModelBase


class LoginViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.email: str = None
        self.password: str = None

    async def load(self):
        form = await self.request.form()
        self.email = form.get('email')
        self.password = form.get('password')
        if not self.email or not self.email.strip():
            self.error = "Your email is required."
        elif not self.password or len(self.password) < 8:
            self.error = "Your password is required and must be at least 8 characters."
        elif not await user_service.authenticate_user(email=self.email, password=self.password):
            self.error = "Email or password is incorrect or user doesn't exist"
