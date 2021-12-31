from utilities import *
import altair as alt


# Function for technical analysis charts.
def technical_analysis(ticker, start, end):
    data = get_stock_data(ticker, start, end)
    name1 = get_company_name_long(ticker)
    data["60 Day MA"] = data['Adj Close'].rolling(window=60).mean()
    sliced_data = data[60::]
    comparison_data = sliced_data[['Adj Close', '60 Day MA']]
    data = comparison_data.reset_index().melt('Date')
    data2 = data.rename(columns={"value": "Amount", "variable": "Measure"}, errors="raise")
    alt_chart = alt.Chart(data2).mark_line().encode(
        x='Date',
        y='Amount',
        color='Measure'
    ).properties(title=f"60 Day MA vs Adj. Close for {name1}", height=500, width=750).interactive()
    st.write(alt_chart)
