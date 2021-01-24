import pandas as pd
import yaml
import os
import json

from pandas import DataFrame
from iexfinance.stocks import Stock

TICKERS = None
CONFIG = None
TOKEN = None

def load_tickers():
    global TICKERS
    TICKERS = pd.read_csv("./data/tickers.csv")

def start():
    global CONFIG, TOKEN
    with open('./config.yaml', 'r') as f:
        try:
            # Read the configuration yaml files
            CONFIG = yaml.full_load(f)

            # Set the API version
            set_sandbox(CONFIG["debug"])

            if CONFIG["debug"]:
                TOKEN = CONFIG["iex"]["sandbox"]["public"]
            else:
                TOKEN = CONFIG["iex"]["production"]["public"]
                
            # Load the company-ticker dataset
            load_tickers()

        except:
            print("Error reading configuration!!!")
            
def is_valid_company(company:str) -> bool:
    return any(TICKERS[TICKERS["company"].str.contains(company, case=False)])

def is_valid_ticker(ticker:str) -> bool:
    return any(TICKERS[TICKERS["symbol"].str.contains(ticker, case=False)])

def find_ticker(kwd:str, limit:int=10) -> pd.Series:
    tickers = TICKERS[TICKERS["company"].str.contains(kwd, case=False)].head(limit)
    # print(tickers["company"])
    if len(tickers) == 0:
        print("Invalid company name")
        return []
    return tickers[["company", "symbol"]]
    
def set_sandbox(debug:bool=False):
    if debug: 
        os.environ["IEX_API_VERSION"] = "sandbox"

def get_stock(stock_name:str, token:str):
    stock = Stock(stock_name.upper(), token=token)
    print(stock.get())

# if __name__ == "__main__":
#     while True:
        
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