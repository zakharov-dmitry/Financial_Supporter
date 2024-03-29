import user_service
from viewmodels.shared.viewmodel import ViewModelBase
from fastapi import Request


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.username: str = None
        self.name: str = None
        self.password: str = None

    async def load(self):
        form = await self.request.form()
        self.username = form.get('email')
        self.name = form.get('name')
        if self.name == '':
            self.name = None  # None instead of empty string
        self.password = form.get('password')

        if not self.username or not self.username.strip():
            self.error = "Your email is required."
        elif not self.password or len(self.password) < 8:
            self.error = "Your password is required and must be at least 8 characters."
        elif await user_service.get_user_by_email(self.username):
            self.error = "That email is already taken. Log in instead?"
