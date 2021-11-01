import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get('/')
@template(template_file='home/index.pt')
def index():
    return {}
