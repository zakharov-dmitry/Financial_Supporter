import requests
import aiohttp


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
    price = data['marketdata_yields']['data'][0][price_index]

    return price


async def get_coupons_for_investment_async(code: str):
    url = f'https://iss.moex.com/iss/statistics/engines/stock/markets/bonds/bondization/{code}.json?iss.meta=off'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            data_index = data['coupons']['columns'].index('coupondate')
            value_index = data['coupons']['columns'].index('value_rub')
            coupons = {item[data_index]: item[value_index] for item in data['coupons']['data']}

    return coupons


async def get_prise_for_investment_async(code: str):
    url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{code}.json?iss.meta=off'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # getting index of the price from the "columns" list
            price_index = data['marketdata_yields']['columns'].index('PRICE')
            # [0] because the list with data is inside of another list
            price = data['marketdata_yields']['data'][0][price_index]

    return price


async def get_ext_investment_data_async(code: str):
    url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities/{code}.json?iss.meta=off'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # getting indexes for needed columns
            title_index = data['securities']['columns'].index('SECNAME')
            value_index = data['securities']['columns'].index('FACEVALUE')
            closing_date_index = data['securities']['columns'].index('MATDATE')
            # [0] because the list with data is inside of another list
            external_data = {'title': data['securities']['data'][0][title_index],
                             'value': data['securities']['data'][0][value_index],
                             'closing_date': data['securities']['data'][0][closing_date_index]}
    return external_data

