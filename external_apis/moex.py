import requests
import aiohttp
import asyncio


def get_coupons_for_investment(code: str):
    url = f'https://iss.moex.com/iss/statistics/engines/stock/markets/bonds/bondization/{code}.json?iss.meta=off'
    r = requests.get(url)
    data = r.json()
    data_index = data['coupons']['columns'].index('coupondate')
    value_index = data['coupons']['columns'].index('value_rub')
    coupons = {item[data_index]: item[value_index] for item in data['coupons']['data']}

    return coupons


def get_prise_for_investment(code: str):
    url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{code}.json?iss.meta=off'
    r = requests.get(url)
    data = r.json()
    # getting index of the price from the "columns" list
    price_index = data['marketdata_yields']['columns'].index('PRICE')
    # [0] because the list with data is inside of another list
    price = data['marketdata_yields']['data']

    return price[0][price_index]


async def get_coupons_for_investment_async(code: str):
    async def _get_all_coupons_recurrently(start_entree: int = 0):
        url = f'https://iss.moex.com/iss/statistics/engines/stock/markets/bonds/bondization/{code}.json?iss.meta=off&start={start_entree}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                page_data = await response.json()
                data_index = page_data['coupons']['columns'].index('coupondate')
                value_index = page_data['coupons']['columns'].index('value_rub')
                coupons = {item[data_index]: item[value_index] for item in page_data['coupons']['data']}

                # calculate total amount of coupons and list trough the pages to get all coupons recurrently
                current_entree = page_data['coupons.cursor']['data'][0][0]
                total_entries = page_data['coupons.cursor']['data'][0][1]
                pagesize = page_data['coupons.cursor']['data'][0][2]
                if current_entree + pagesize < total_entries:
                    coupons.update(await _get_all_coupons_recurrently(current_entree + pagesize))

        return coupons

    all_coupons = await _get_all_coupons_recurrently()
    # find the last defined coupon to use it as a forecast for undefined coupons
    last_defined_coupon = list(filter(None, all_coupons.values()))[-1]
    # replace all undefined coupons with forecast
    all_coupons = {key: (value if value is not None else last_defined_coupon) for key, value in all_coupons.items()}

    return all_coupons


async def get_prise_for_investment_async(code: str):
    url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{code}.json?iss.meta=off'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # getting index of the price from the "columns" list
            price_index = data['marketdata_yields']['columns'].index('PRICE')
            accrued_coupon_income_index = data['securities']['columns'].index('ACCRUEDINT')
            # [0] because the list with data is inside of another list
            current_data = {'accrued_coupon_income': data['securities']['data'][0][accrued_coupon_income_index],
                            'price':  data['marketdata_yields']['data'][0][price_index]}

    return current_data


async def get_ext_investment_data_async(code: str):
    """call external MOEX API and return a dict with title, value, closing date for given position code"""
    url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{code}.json?iss.meta=off'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # getting indexes for needed columns
            title_index = data['securities']['columns'].index('SECNAME')
            value_index = data['securities']['columns'].index('FACEVALUE')
            closing_date_index = data['securities']['columns'].index('MATDATE')
            accrued_coupon_income_index = data['securities']['columns'].index('ACCRUEDINT')
            # [0] because the list with data is inside of another list
            external_data = {'title': data['securities']['data'][0][title_index],
                             'value': data['securities']['data'][0][value_index],
                             'closing_date': data['securities']['data'][0][closing_date_index],
                             'accrued_coupon_income': data['securities']['data'][0][accrued_coupon_income_index]}

    return external_data


# results = asyncio.run(get_coupons_for_investment_async("RU000A1022E6"))
# print(results)
# print(asyncio.run(get_coupons_for_investment_async("RU000A101XD8")))
print(asyncio.run(get_ext_investment_data_async("RU000A100D89")))