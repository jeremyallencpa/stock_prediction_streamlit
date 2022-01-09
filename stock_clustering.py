import pandas_datareader as web
import datetime as dt
from yahoo_fin import stock_info as si
import numpy as np
from scipy.cluster.vq import kmeans, vq
import pandas as pd
from math import sqrt
from sklearn.cluster import KMeans
import altair as alt
import streamlit as st


# Cache dataframe
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def stock_clustering_kmeans():
    # Stock clusters for this program are the stock tickers in the Dow Jones Industrial Index.
    # Code allows for additional indexes to be added at a later time.
    stocks = si.tickers_dow()
    # Set start and end times to one year from today.
    start = dt.datetime.now() - dt.timedelta(days=365 * 1)
    end = dt.datetime.now()
    # Try statement for pulling stock data.
    try:
        prices_df = web.DataReader(list(stocks), 'yahoo', start, end)['Adj Close']
        prices_df.reset_index(inplace=True)
        prices_df.drop(['Date'], axis=1, inplace=True)

        # Calculate returns and volatility.
        returns = prices_df.pct_change().mean() * 252
        returns = pd.DataFrame(returns)
        returns.columns = ['Returns']
        returns['Volatility'] = prices_df.pct_change().std() * sqrt(252)

        # Format the data as a numpy array to feed into the K-Means algorithm
        data = np.asarray([np.asarray(returns['Returns']), np.asarray(returns['Volatility'])]).T

        # Generate k-means clusters. Range is from 2 to 21 in this case. A chart will then be generated showing
        # the inertia depending upon the number of clusters. Based upon the data, the inertia seems to become
        # linear at k = 10. Therefore, this will be the number used to generate the clusters.
        X = data
        inertia = []
        k_values = []
        for k in range(2, 21):
            k_means = KMeans(n_clusters=k)
            k_means.fit(X)
            inertia.append(k_means.inertia_)
            k_values.append(k)
        st.write("Sum of squared errors for distortions")
        # Create data frame to hold distortion values
        inertia_array = np.asarray(inertia)
        inertia_df = pd.DataFrame(inertia_array, columns=["Distortions"])
        k_values_array = np.asarray(k_values)
        k_values_df = pd.DataFrame(k_values_array, columns=['K-Values'])
        inertia_df['K-Values'] = k_values_df
        # Graph distortion values and pick K value
        comparison_chart = alt.Chart(inertia_df).mark_line(color='green').encode(
            x='K-Values',
            y='Distortions'
        ).properties(title=f"Elbow curve for selecting K-value for K-means clustering", height=600,
                     width=800).interactive()
        st.altair_chart(comparison_chart)

        # Computing K-Means with K = 10 (10 clusters)
        centroids, _ = kmeans(data, 10)
        # Assign each sample to a cluster
        idx, _ = vq(data, centroids)
        returns.reset_index()
        returns['Clusters'] = idx
        returns.reset_index(inplace=True)

        # Plot data
        domain = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        range_ = ['red', 'orange', 'yellow', 'green', 'blue', 'pink', 'purple', 'gold', 'indigo', 'white']
        scatter = alt.Chart(returns).mark_circle(size=60).encode(
            x='Returns',
            y='Volatility',
            color=alt.Color('Clusters', legend=None, scale=alt.Scale(domain=domain, range=range_)),
            tooltip=['Symbols', 'Clusters', 'Returns', 'Volatility']
        ).properties(title=f"K-Means Clustering", height=450, width=670).interactive()
        st.write(scatter)
        st.subheader("K-Means Clustering Table")
        st.write(returns.sort_values(by='Clusters'))

        # Create button to download returns  and clusters data.
        csv = convert_df(returns)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='cluster_data.csv',
            mime='text/csv',
        )
    except ValueError:
        st.error("Error fetching data, please try running again.")
