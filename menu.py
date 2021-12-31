from stock_predictor import *
from total_returns import *
from volume_analysis import *
from technical_analysis import *
from dashboard import *


# Menu function to display menu options.
def menu():
    page = st.sidebar.selectbox(
        "Select a Menu Option",
        [
            "Stock Prediction",
            "Stock Indexes",
            "Total Returns Analysis",
            "Volume Analysis",
            "Technical Analysis"
        ]
    )

    # First page
    if page == "Stock Indexes":
        dashboard()

    # Second Page
    elif page == "Stock Prediction":
        ticker = st.text_input("Enter valid stock ticker:")
        today = dt.datetime.now()
        five_years_ago = today - dt.timedelta(weeks=260)
        start = five_years_ago
        end = today
        if st.button('Run Stock Prediction Program'):
            check_ticker = check_valid_ticker(ticker)
            check_valid_dates = check_date_range(start, end)
            if check_ticker & check_valid_dates:
                stock_predictor(ticker, start, end)
            elif not check_ticker:
                st.error("Invalid ticker. Try again.")
            elif not check_valid_dates:
                st.error("Invalid date range. "
                         "Ensure start date is before end date and "
                         "that both dates are not on weekends.")

    # Third Page
    elif page == "Total Returns Analysis":
        ticker1 = st.text_input("Enter valid stock ticker")
        ticker2 = st.selectbox(
            'Select comparison index',
            ('^GSPC', '^DJI', '^IXIC', 'BTC-USD'))
        max_value = dt.datetime.now()
        min_value = max_value - dt.timedelta(days=30)
        start = st.date_input("Start Date:", value=min_value, min_value=None, max_value=min_value)
        end = st.date_input("End Date:", value=None, min_value=None, max_value=max_value)
        if st.button('View Cumulative Returns'):
            check_ticker = check_valid_ticker(ticker1)
            check_valid_dates = check_date_range(start, end)
            if check_ticker & check_valid_dates:
                total_returns_altair(ticker1, ticker2, start, end)
            elif not check_ticker:
                st.error("Invalid ticker. Try again.")
            elif not check_valid_dates:
                st.error("Invalid date range. "
                         "Ensure start date is before end date and "
                         "that both dates are not on weekends.")

    # Fourth Page
    elif page == "Volume Analysis":
        ticker = st.text_input("Enter valid stock ticker")
        max_value = dt.datetime.now()
        min_value = max_value - dt.timedelta(days=30)
        start = st.date_input("Start Date:", value=min_value, min_value=None, max_value=max_value)
        end = st.date_input("End Date:", value=None, min_value=None, max_value=max_value)
        if st.button('View Volume Analysis'):
            check_ticker = check_valid_ticker(ticker)
            check_valid_dates = check_date_range(start, end)
            if check_ticker & check_valid_dates:
                volume_analysis_altair(ticker, start, end)
            elif not check_ticker:
                st.error("Invalid ticker. Try again.")
            elif not check_valid_dates:
                st.error("Invalid date range. "
                         "Ensure start date is before end date and "
                         "that both dates are not on weekends.")

    # Fifth page
    elif page == "Technical Analysis":
        ticker = st.text_input("Enter valid stock ticker")
        today = dt.datetime.now()
        six_months_ago = today - dt.timedelta(days=180)
        max_value = dt.datetime.now()
        start = st.date_input("Start Date:", value=six_months_ago, min_value=None, max_value=six_months_ago)
        end = st.date_input("End Date:", value=None, min_value=None, max_value=max_value)
        if st.button('View Technical Analysis'):
            check_ticker = check_valid_ticker(ticker)
            check_valid_dates = check_date_range(start, end)
            if check_ticker & check_valid_dates:
                technical_analysis(ticker, start, end)
            elif not check_ticker:
                st.error("Invalid ticker. Try again.")
            elif not check_valid_dates:
                st.error("Invalid date range. "
                         "Ensure start date is before end date and "
                         "that both dates are not on weekends.")
