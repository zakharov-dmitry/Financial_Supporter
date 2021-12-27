import fastapi
from fastapi import APIRouter, Request, status
from fastapi_chameleon import template
from sqlalchemy.exc import IntegrityError


import investment_service
from viewmodels.investment.investment_viewmodel import InvestmentViewModel

router = APIRouter()


@router.get("/investment/add")
@template(template_file="investment/investment_add.pt")
def create_investment(request: Request):
    vm = InvestmentViewModel(request)
    return vm.to_dict()


@router.post("/investment/add")
@template(template_file="investment/investment_add.pt")
async def add_investment(request: Request):
    vm = InvestmentViewModel(request)
    await vm.load()
    if vm.error:
        return vm.to_dict()
    try:
        await investment_service.add_investment_for_user(
            title=vm.title,
            code=vm.code,
            amount=vm.amount,
            value=vm.value,
            owner_email=vm.owner.email,
            purchase_date=vm.purchase_date,
            avg_prise=vm.avg_prise,
            purchase_prise=vm.purchase_prise,
            closing_date=vm.closing_date
        )
        response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return response
    except IntegrityError:
        vm.error = f"Investment with this ID already exists for {vm.owner.name}"
