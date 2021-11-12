import fastapi.responses
from fastapi import APIRouter, Request, status
from fastapi_chameleon import template

from services import user_service
from viewmodels.account. register_viewmodel import RegisterViewModel

router = APIRouter()


@router.get("/account/register")
@template()
def register(request: Request):
    vm = RegisterViewModel(request)
    return vm.to_dict()

@router.post("/account/register")
@template()
async def register(request: Request):
    vm = RegisterViewModel(request)
    await vm.load()
    if vm.error:
        return vm.to_dict()
    account = await user_service.create_new_user(vm.email, vm.name, vm.password)
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response
