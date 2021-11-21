import fastapi
from fastapi import APIRouter, Request, status
from fastapi_chameleon import template
from sqlalchemy.exc import IntegrityError

from services import investment_service
from viewmodels.investment.investment_viewmodel import InvestmentViewModel

router = APIRouter()


@router.get("/investment/add")
@template(template_file="investment/investment_details.pt")
def create_investment(request: Request):
    vm = InvestmentViewModel(request)
    return vm.to_dict()


@router.post("/investment/add")
@template(template_file="investment/investment_details.pt")
async def add_investment(request: Request):
    vm = InvestmentViewModel(request)
    await vm.load()
    print(vm.to_dict())
    if vm.error:
        return vm.to_dict()
    try:
        await investment_service.add_investment_for_user(
            title=vm.title,
            id=vm.id,
            amount=vm.amount,
            coupon=vm.coupon,
            owner_email=vm.owner.email
        )
        response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    except IntegrityError:
        vm.error = f"Investment with this ID already exists for {vm.owner.name}"
