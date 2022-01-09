from stock_predictor import *
from total_returns import *
from volume_analysis import *
from technical_analysis import *
from stock_indexes import *
from stock_clustering import *
from portfolio_models import *


# Menu function to display menu options.
def menu():
    page = st.sidebar.selectbox(
        "Select a Menu Option",
        [
            "Stock Clustering",
            "Portfolio Builder",
            "Stock Prediction",
            "Stock Indexes",
            "Total Returns Analysis",
            "Volume Analysis",
            "Technical Analysis"
        ]
    )

    # Stock index page
    if page == "Stock Indexes":
        dashboard()

    # Stock Prediction Page
    elif page == "Stock Prediction":
        ticker = st.text_input("Enter valid stock ticker:")
        today = dt.datetime.now()
        one_year_ago = today - dt.timedelta(weeks=260)
        start = one_year_ago
        end = today
        if st.button('Run Stock Prediction Program'):
            check_ticker = check_valid_ticker(ticker)
            if check_ticker:
                stock_predictor(ticker, start, end)
            elif not check_ticker:
                st.error("Invalid ticker. Try again.")

    # Stock Clustering Page
    elif page == "Stock Clustering":
        st.header("Stock Clustering Using K-Means for the Dow Jone Industrial Index")
        st.write("Note: this process may take several minutes to run.")
        if st.button('Run Stock Clustering Program'):
            stock_clustering_kmeans()

    # Portfolio builder page
    elif page == "Portfolio Builder":
        st.header("Portfolio Builder Using Monte Carlo Simulations")
        st.write("Note: this process may take several minutes to run.")
        st.write("Enter list of tickers separated by commas and a space below. For example: AMZN, NFLX, AAPL, GOOG")
        # Get list of tickers
        tickers_list = st.text_input("Enter list of tickers separated by commas and a space here:")
        if st.button('Run Portfolio builder'):
            # Converting string to list
            tickers = tickers_list.strip('][').split(', ')
            # Check tickers
            invalid_tickers = []
            for ticker in tickers:
                if not check_valid_ticker(ticker):
                    invalid_tickers.append(ticker)
                else:
                    pass
            if (len(invalid_tickers)) != 0:
                st.error(f"Invalid tickers entered. The following tickers are invalid: {invalid_tickers}")
            # Run program if tickers are all valid.
            else:
                today = dt.datetime.now()
                one_year_ago = today - dt.timedelta(weeks=52)
                start = one_year_ago
                end = today
                weights = portfolio_builder(tickers, start, end)
                cum_returns = calc_portfolio_cumulative_returns(tickers, weights, start, end)
                cum_returns_df = cum_returns[['Date', 'Cumulative Returns $1,000', 'Symbol']]
                index_df = total_returns('^DJI', start, end)
                comparison_data = pd.concat(
                    [cum_returns_df[['Date', 'Cumulative Returns $1,000', 'Symbol']],
                     index_df[['Date', 'Cumulative Returns $1,000', 'Symbol']],
                     ],
                    axis=0)
                comparison_chart = alt.Chart(comparison_data).mark_line().encode(
                    x='Date',
                    y='Cumulative Returns $1,000',
                    color='Symbol'
                ).properties(title=f"Cumulative returns of $1,000 invested in portfolio vs index", height=500,
                             width=750).interactive()
                st.altair_chart(comparison_chart)

                # Create a list of portfolio values
                tickers_array = np.asarray(tickers)
                tickers_df = pd.DataFrame(tickers_array, columns=["Ticker"])
                weights_df = pd.DataFrame(weights, columns=["Weights"])
                tickers_df['Weights'] = weights_df['Weights']
                st.write("Here are the relative weights of the generated portfolio by ticker.")
                st.write(tickers_df)

    # Total Returns Analysis Page
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

    # Volume Analysis Page
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

    # Technical Analysis page
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
