import pandas as pd
import yaml
import os
import json
import asyncio
import aiohttp


from pandas import DataFrame
from iexfinance.stocks import Stock
# from requests import async

SESSION = None

TICKERS = None
CONFIG = None
TOKEN = None
VERSION = None
URL = None


async def create_session():
    global SESSION
    SESSION = aiohttp.ClientSession()


def load_tickers():
    global TICKERS
    TICKERS = pd.read_csv("./data/tickers.csv")


def start():
    global CONFIG, TOKEN, VERSION, URL
    with open('./config.yaml', 'r') as f:
        try:
            # Read the configuration yaml files
            CONFIG = yaml.full_load(f)

            # Set the iex environment mode
            VERSION = "sandbox" if CONFIG["debug"] else "production"
            TOKEN = CONFIG["iex"][VERSION]["public"]
            URL = CONFIG["iex"][VERSION]["URL"]

            # Set the API version
            set_sandbox(CONFIG["debug"])

            # Load the company-ticker dataset
            load_tickers()

        except Exception as e:
            print("Error reading configuration!!!", e)


def is_valid_company(company: str) -> bool:
    companies = TICKERS[TICKERS["company"].str.contains(
        company, case=False)]["company"]
    return len(companies) > 0


def is_valid_ticker(ticker: str) -> bool:
    symbols = TICKERS[TICKERS["symbol"].str.contains(
        ticker, case=False)]["symbol"]
    return len(symbols) > 0


def find_ticker(kwd: str, limit: int = 10) -> pd.Series:
    tickers = TICKERS[TICKERS["company"].str.contains(
        kwd, case=False)].head(limit)
    # print(tickers["company"])
    if len(tickers) == 0:
        print("Invalid company name")
        return []
    return tickers[["company", "symbol"]]


async def fetch_data(url: str, **kwargs) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.request(
                method="get",
                url=url,
                **kwargs
            )
            r.raise_for_status()
            data = await r.json()
            return data
    except Exception as e:
        print("Could not fetch IEX data", e)
        return None


async def get_stock_information(symbol: str, range: str = "1m", **kwargs):
    url = f"{URL}/stock/{symbol}/batch?types=quote,chart&range={range}&token={TOKEN}"
    r = await fetch_data(url, **kwargs)
    return r


def set_sandbox(debug: bool = False):
    if debug:
        os.environ["IEX_API_VERSION"] = "sandbox"


def get_stock(stock_name: str, token: str):
    stock = Stock(stock_name.upper(), token=token)
    print(stock.get())


async def main():
    start()
    while True:
        ticker = input("Enter a stock name: ")
        if is_valid_ticker(ticker):
            data = await get_stock_information(ticker)
        print(is_valid_ticker(ticker))

if __name__ == "__main__":
    asyncio.run(main())
    # break

#         # Load the configuration and ticker information
#         start()
#         # stock_name = input("Enter a stock name: ")
#         # get_stock(stock_name, token)

#         company_name = input("Enter a company name: ")
#         tickers = find_ticker(company_name)

#         if len(tickers) > 0:
#             for company, symbol in tickers.values:
#                 print(f"\033[1;32;40m\t{company:<60} {symbol}")
#             print("\033[0m ", end="")
#             print()
#         # get_ticker(stock_name)
