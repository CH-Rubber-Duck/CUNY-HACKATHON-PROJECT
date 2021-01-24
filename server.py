import iex
import json
from fastapi import FastAPI

iex.start()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/company/{company_name}")
async def get_company(company_name: str):
    tickers = iex.find_ticker(company_name.replace('-', ' ')).values
    return tickers

@app.get("/stocks/{ticker}")
async def get_company(ticker: str):
    tickers = iex.find_ticker(ticker.replace('-', ' ')).values
    return tickers