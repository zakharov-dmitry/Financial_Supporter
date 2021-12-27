from datetime import datetime
from typing import List, Optional
from fastapi import Request

from models.investment import Investment
from investment_service import all_investments_for_user
from moex import get_coupons_for_investment, get_prise_for_investment
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
        self.positions: Optional[List] = None

    async def load(self):
        # rough data from db
        investments_from_db = await all_investments_for_user()
        # casting Investment from DB to another extended class InvestmentWithCalculations
        investments_with_calculation = [InvestmentWithCalculations(i) for i in investments_from_db]
        [i.calculate_values() for i in investments_with_calculation]
        combined_investments = combine_investments(investments_with_calculation)
        self.positions = [Position(*item) for item in combined_investments.items()]
        [position.formatting_values() for position in self.positions]


class InvestmentWithCalculations:
    def __init__(self, investment):
        self.i: Investment = investment
        self.paid_coup: dict = None
        self.curr_pris: float = None
        self.curr_totl_incm: float = None
        self.curr_intr: float = None
        self.curr_annl_intr: float = None
        self.clos_totl_incm: float = None
        self.clos_intr: float = None
        self.clos_annl_intr: float = None
        self.hold_year: float = None

    def calculate_values(self):
        # get all coupons for investment as dict date:money
        all_coupons = get_coupons_for_investment(self.i.code)
        self.curr_pris = get_prise_for_investment(self.i.code)

        # check if the coupon can be paid in the future, coupon date after the purchase date
        def _coupon_can_be_paid(coupon):
            start_date = self.i.purchase_date
            coupon_date = datetime.strptime(coupon, "%Y-%m-%d").date()
            return start_date < coupon_date

        # sum of all coupons in rubles that can be paid for one item, if item will be hold till the end
        sum_all_coupons = sum([value for key, value in all_coupons.items() if _coupon_can_be_paid(key)])

        # checks that coupon is already paid, coupon date between the purchase date and current date
        def _coupon_is_paid(coupon):
            start_date = self.i.purchase_date
            end_date = datetime.now().date()
            coupon_date = datetime.strptime(coupon, "%Y-%m-%d").date()
            return start_date < coupon_date < end_date

        # dict of all coupons that are already paid for investment
        self.paid_coup = {key: value for key, value in all_coupons.items() if _coupon_is_paid(key)}
        # sum of all coupons in rubles that are already paid for investment
        income_coupons = sum(self.paid_coup.values())

        # earned money for current investment till now
        self.curr_totl_incm = self.i.amount * (
                income_coupons + self.i.value * self.curr_pris / 100) - self.i.purchase_prise
        # % earned for current investment till now
        self.curr_intr = self.curr_totl_incm / self.i.purchase_prise

        # how many years the investment is in possession till now, +1 for avoid division by zero
        self.hold_year = ((datetime.now().date() - self.i.purchase_date).days + 1) / 365
        # annual % earned for current investment till now
        self.curr_annl_intr = self.curr_intr / self.hold_year

        # earned money for current investment if it will be held till the closing
        self.clos_totl_incm = self.i.amount * (sum_all_coupons + self.i.value) - self.i.purchase_prise
        # % earned for current investment if it will be held till the closing
        self.clos_intr = self.clos_totl_incm / self.i.purchase_prise

        # how many years the investment will be in possession till the closing
        holding_year_till_end = (self.i.closing_date - self.i.purchase_date).days / 365
        # annual % earned for current investment if it will be held till the closing
        self.clos_annl_intr = self.clos_intr / holding_year_till_end

        return self

    def formatting_values(self):
        self.curr_totl_incm = f"{int(self.curr_totl_incm)}"
        self.curr_annl_intr = f"{self.curr_annl_intr * 100:.2f}"
        self.clos_totl_incm = f"{int(self.clos_totl_incm)}"
        self.clos_annl_intr = f"{self.clos_annl_intr * 100:.2f}"
        self.hold_year = f"{self.hold_year:.2f}"

    # TODO will not work after formatting - refactoring needed
        def __repr__(self):
            info = f"""
            Title                  : {self.i.title}
            Amount                 : {self.i.amount}
            Purchase Date          : {self.i.purchase_date}
            Average Purchase Prise : {self.i.avg_prise:.2f}%
            Purchase Prise         : {self.i.purchase_prise}
            Closing Date           : {self.i.closing_date}
            Paid Coupons           : {self.paid_coup}
            Current Average Prise  : {self.curr_pris:.2f}%
            Current Total Income   : {self.curr_totl_incm:.2f}
            Current Interests      : {self.curr_intr * 100:.2f}%
            Current Annual Interest: {self.curr_annl_intr * 100:.2f}%
            Closing Total Income   : {self.clos_totl_incm:.2f}
            Closing Interest       : {self.clos_intr * 100:.2f}%
            Closing Annual Interest: {self.clos_annl_intr * 100:.2f}%
            -----------------------------------
            """
            return info



def combine_investments(investments_with_calculations: List[InvestmentWithCalculations]):
    unique_investments_codes = set([investment.i.code for investment in investments_with_calculations])
    unique_investments_dict = {key: [] for key in unique_investments_codes}
    # TODO Refactor into default dict, should be faster
    [unique_investments_dict[investment.i.code].append(investment) for investment in investments_with_calculations]
    return unique_investments_dict


class Position:
    def __init__(self, code: str, investments_with_calculations: List[InvestmentWithCalculations]):
        self.code = code
        self.investments = investments_with_calculations
        # take the title from the first item in the list, all equal
        self.title = investments_with_calculations[0].i.title
        self.amount = sum([i.i.amount for i in investments_with_calculations])
        self.avg_prise = sum([i.i.avg_prise * i.i.amount for i in investments_with_calculations])/self.amount
        self.current_prise = investments_with_calculations[0].curr_pris
        self.current_income = sum([i.curr_totl_incm for i in investments_with_calculations])
        self.current_interest = sum([i.curr_annl_intr * i.i.amount for i in investments_with_calculations])/self.amount
        self.closing_income = sum([i.clos_totl_incm for i in investments_with_calculations])
        self.closing_interest = sum([i.clos_annl_intr * i.i.amount for i in investments_with_calculations])/self.amount
        self.closing_date = investments_with_calculations[0].i.closing_date

    def formatting_values(self):
        self.avg_prise = f"{self.avg_prise:.2f}"
        self.current_income = f"{int(self.current_income)}"
        self.current_interest = f"{self.current_interest * 100:.2f}"
        self.closing_income = f"{int(self.closing_income)}"
        self.closing_interest = f"{self.closing_interest * 100:.2f}"
        [i.formatting_values() for i in self.investments]
        return self

    def __repr__(self):
        return f"{self.title}:{self.amount} with % on closing: {self.closing_interest}"