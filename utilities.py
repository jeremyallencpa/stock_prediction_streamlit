import streamlit as st
import yfinance as yf
from time import sleep
import requests


# Function to get stock data in the form of a data frame. Yahoo Finance will reject too many requests in a row
# so a sleep setting is implemented here between requests to try and prevent getting a connection error.
def get_stock_data(ticker, start, end):
    data_load_state = st.text("Data loading...")
    sleep(1)
    try:
        data = yf.download(ticker, start, end)
        print(f"Successfully downloaded data for {ticker} from {start} to {end}")
        if data.empty:
            st.error("Check that input dates are not weekends.")
        else:
            data_load_state.text("")
            return data
    except TimeoutError:
        st.error("Connection error, please try to refresh.")
    except ConnectionError:
        st.error("Connection error, please try to refresh.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error, please try to refresh.")
    except WindowsError:
        st.error("Connection error, please try to refresh.")
    except Exception as e:
        st.write(e)
        st.error("Connection error, please try to refresh.")


# Function to check that the ticker is a valid ticker.
def check_valid_ticker(ticker):
    try:
        ticker_string = yf.Ticker(str(ticker))
        if ticker_string.info['regularMarketPrice'] is None:
            return False
        else:
            return True
    except ValueError:
        st.error("Invalid ticker. Try again.")


# Function to return the long name of a company. For example, a ticker symbol of 'FB' will return the long name
# of 'Meta Platforms, Inc.'
def get_company_name_long(ticker):
    company_name = yf.Ticker(ticker)
    company_name_long = company_name.info['longName']
    return company_name_long


# Function to get index long name.
def get_index_name(ticker):
    if ticker == '^GSPC':
        return "S&P 500 Index"
    elif ticker == '^DJI':
        return "Dow Jones Industrial Index"
    elif ticker == '^IXIC':
        return "NASDAQ Composite"
    else:
        return "BTC-USD"


# Function to check date ranges are valid.
def check_date_range(start, end):
    check_weekend_start = check_weekend(start)
    check_weekend_end = check_weekend(end)

    if start >= end:
        return False
    elif check_weekend_start or check_weekend_end:
        return False
    else:
        return True


# Function to make sure dates selected do not fall on weekends.
def check_weekend(date):
    check_date = date.weekday()
    if check_date == 5:
        return True
    elif check_date == 6:
        return True
    else:
        return False
