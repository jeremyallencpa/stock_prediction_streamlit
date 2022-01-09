import datetime as dt
from utilities import *
import altair as alt


# Function to create a chart for a given index on the home page.
def display_index(ticker, ticker_color, index_name):
    today = dt.datetime.now()
    one_month_view = today - dt.timedelta(weeks=260)
    start = one_month_view
    end = today
    data = get_stock_data(ticker, start, end).reset_index()
    index_chart = alt.Chart(data).mark_line(color=ticker_color).encode(
        x='Date',
        y='Close'
    ).properties(title=f"{index_name} - 5 Year Chart", height=600, width=800).interactive()
    return index_chart


# Function to display the dashboard.
def dashboard():
    # Generate header. Provide a select box with 4 indexes: S&P500, DJI, Nasdaq and BTC
    ticker = st.selectbox(
        'Select index',
        ('^GSPC', '^DJI', '^IXIC', 'BTC-USD'))
    if ticker == '^GSPC':
        spx = display_index('^GSPC', 'Red', "S&P 500 Index")
        st.altair_chart(spx)
    elif ticker == '^DJI':
        dji = display_index('^DJI', 'Purple', "Dow Jones Industrial Index")
        st.altair_chart(dji)
    elif ticker == '^IXIC':
        nasdaq = display_index('^IXIC', 'Green', "NASDAQ Composite")
        st.altair_chart(nasdaq)
    else:
        btc = display_index('BTC-USD', 'Orange', "BTC-USD")
        st.altair_chart(btc)
