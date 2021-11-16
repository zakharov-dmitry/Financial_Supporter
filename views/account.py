import asyncio

import fastapi.responses
from fastapi import APIRouter, Request, status, HTTPException
from fastapi_chameleon import template

from infastructure.security import login_for_access_token
from services import user_service
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel

router = APIRouter()


@router.get("/account/login")
@template()
def login(request: Request):
    vm = LoginViewModel(request)
    return vm.to_dict()


@router.post("/account/login")
@template()
async def login(request: Request):
    vm = LoginViewModel(request)
    await vm.load()
    if vm.error:
        await asyncio.sleep(5)
        return vm.to_dict()
    try:
        response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        await login_for_access_token(response=response, form_data=vm)
        return response
    except HTTPException as Error:
        vm.error = Error.detail
        return vm.to_dict()


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
    account = await user_service.create_new_user(vm.username, vm.name, vm.password)
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return response
