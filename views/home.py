import fastapi
from fastapi_chameleon import template
from fastapi import Request

from viewmodels.home.index_viewmodel import IndexViewModel

router = fastapi.APIRouter()


@router.get('/')
@template(template_file='home/index.pt')
def index(request: Request):
    vm = IndexViewModel(request)
    return vm.to_dict()
