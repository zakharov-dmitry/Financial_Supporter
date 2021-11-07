import fastapi
from fastapi_chameleon import template
from fastapi import Request

from viewmodels.home.index_viewmodel import IndexViewModel

router = fastapi.APIRouter()


@router.get('/')
@template()
async def index(request: Request):
    vm = IndexViewModel(request)
    await vm.load()
    return vm.to_dict()
