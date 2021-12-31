from utilities import *
import altair as alt


# Function to display volume for a selected stock.
def volume_analysis_altair(ticker, start, end):
    try:
        data = get_stock_data(ticker, start, end).reset_index()
        name1 = get_company_name_long(ticker)
        comparison_chart = alt.Chart(data).mark_line(color='green').encode(
            x='Date',
            y='Volume'
        ).properties(title=f"Volume traded for {name1}", height=600,
                     width=800).interactive()
        st.altair_chart(comparison_chart)
    except ConnectionError:
        st.error("Connection Error, please try refreshing.")
