import pandas as pd
from utilities import *
import altair as alt


# Function to calculate total returns
def total_returns(ticker, start, end):
    try:
        data = get_stock_data(ticker, start, end).reset_index()
        data["Returns"] = data['Adj Close'].pct_change(1)[1:]
        data["Cumulative Returns"] = data["Returns"].cumsum() + 1
        data["Cumulative Returns $1,000"] = data["Cumulative Returns"] * 1000
        data["Symbol"] = ticker
        return data
    except AttributeError:
        st.error("Connection Error, try refreshing.")
    except TypeError:
        st.error("Connection Error, try refreshing.")


# Function to display total returns between a stock and an index in a chart.
def total_returns_altair(ticker1, ticker2, start, end):
    df1 = total_returns(ticker1, start, end)
    df2 = total_returns(ticker2, start, end)
    comparison_data = pd.concat(
        [df1[['Date', 'Cumulative Returns $1,000', 'Volume', 'Symbol']],
         df2[['Date', 'Cumulative Returns $1,000', 'Volume', 'Symbol']],
         ],
        axis=0)
    name1 = get_company_name_long(ticker1)
    name2 = get_index_name(ticker2)
    comparison_chart = alt.Chart(comparison_data).mark_line().encode(
        x='Date',
        y='Cumulative Returns $1,000',
        color='Symbol'
    ).properties(title=f"Cumulative returns of $1,000 invested in {name1} vs. {name2}", height=500,
                 width=750).interactive()
    st.altair_chart(comparison_chart)
