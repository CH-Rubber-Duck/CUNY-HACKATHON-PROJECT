import pandas as pd
import yaml
import os
import requests
import json

from iexfinance.stocks import Stock

TICKER_SYMBOL_API_ENDPOINT = "https://ticker-2e1ica8b9.now.sh/keyword/"

def get_tickers(kwd:str) -> str:
    with open('./data/tickers.json', 'r') as f:
        try:
            return json.load(f)
        except:
            print("Error reading tickers!!!")

def load_config() -> any:
    with open('./config.yaml', 'r') as f:
        try:
            return yaml.full_load(f)
        except:
            print("Error reading configuration!!!")
    
def set_sandbox(debug:bool=False):
    if debug: 
        os.environ["IEX_API_VERSION"] = "sandbox"

def get_stock(stock_name:str, token:str):
    stock = Stock(stock_name.upper(), token=token, )
    print(stock.get_price())
    
    

if __name__ == "__main__":
    while True:
        
        # Load the configuration from the YAML file
        config = load_config()

        # Load all tickers from the dataset
        tickers = get_tickers()


        # Set the API version
        set_sandbox(config["debug"])

        token = config["iex"]["sandbox"]["public"]
        stock_name = input("Enter a stock name: ")
        get_stock(stock_name, token)
        # get_ticker(stock_name)