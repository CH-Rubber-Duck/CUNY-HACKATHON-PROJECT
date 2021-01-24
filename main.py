import iex
import json
import asyncio
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Start IEX API
loop = asyncio.get_event_loop()
loop.create_task(iex.start())

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/company/{company_name}")
async def get_company(company_name: str):
    tickers = iex.find_ticker(company_name.replace('-', ' ')).values
    return tickers

@app.get("/stocks/{ticker}/")
async def get_company(ticker: str, drange:str="1m"):
    print(drange)
    if not iex.is_valid_ticker(ticker):
        raise HTTPException(status_code=404, detail="Item not found")
    
    data = await iex.get_stock_information(ticker, drange)
    return data

@app.get("/crypto/{name}")
async def get_company(ticker: str):
    if not iex.is_valid_ticker(ticker):
        raise HTTPException(status_code=404, detail="Item not found")
    
    data = await iex.get_stock_information(ticker)
    return data