# https://github.com/NavdeepD2/Stocks-With-RSI-Below-30-with-Python
import os
import time
from nsetools import Nse
import yfinance as yf
import asyncio
from pyppeteer import launch

# Define the list of stocks
stocks = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "DUMMYREL",
    "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITC",
    "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LTIM", "LT",
    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE",
    "SBILIFE", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS",
    "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"
]

# Function to check if a stock is trading below RSI 40 and take a screenshot of the stock chart
async def check_rsi_and_screenshot(stock_symbol):
    try:
        stock_data = yf.Ticker(stock_symbol + ".NS")
        df = stock_data.history(period="max", interval="1d")

        if len(df) >= 14:
            # Calculate RSI
            delta = df['Close'].diff(1)
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # Check if RSI is below 30
            if rsi.iloc[-1] < 30:
                browser = await launch(headless=True)
                page = await browser.newPage()
                await page.goto(f'https://finance.yahoo.com/quote/{stock_symbol}.NS')
                await asyncio.sleep(5)  # Wait for the page to load (adjust as needed)
                await page.screenshot({'path': f'{stock_symbol}_chart.png'})
                await browser.close()
                print(f"{stock_symbol} - RSI below 40. Screenshot saved.")
        else:
            print(f"{stock_symbol} - Not enough data for RSI calculation.")
    except Exception as e:
        print(f"Error checking {stock_symbol}: {e}")


# Initialize NSE object
nse = Nse()


# Create an event loop to run the async functions
async def main():
    for stock_symbol in stocks:
        await check_rsi_and_screenshot(stock_symbol)


# Run the event loop
asyncio.get_event_loop().run_until_complete(main())

print("Task completed.")
