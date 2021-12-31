import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from keras.models import Sequential
from keras.layers import Dense, LSTM
from utilities import *
import altair as alt


# Function to create a model which will predict the stock price for the next day.
def stock_predictor(ticker, start, end):
    # Variable to hold the long name of a specific ticker.
    name = get_company_name_long(ticker)
    # Set seed to produce consistent results.
    np.random.seed(8)
    # Get the stock data
    df = get_stock_data(ticker, start, end)
    # Create new dataframe with only close column
    data = df.filter(['Close'])
    # Convert to numpy array
    dataset = data.values
    # Get the number of rows to train the model on. In this case, we selected 80% of the data (4 years) to train
    # the model with. This number can be shifted either up or down to see how that would change the results
    # of the model.
    training_data_len = math.ceil(len(dataset) * .8)
    # Scale the data - this will squeeze the values to be between 0 and 1 for processing by the model.
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    # Create the scaled training dataset
    train_data = scaled_data[0:training_data_len, :]
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])
    # Convert the x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)
    # Reshape the x_train dataset
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    # Train the model. Here we set the epochs to 1 but this number can be anything in the range of 1 - N. However,
    # this causes the processing of the model to increase at a rate of O(N) meaning 10 epochs will take approximately
    # 10 times as much time to process as 1 epoch.
    model.fit(x_train, y_train, batch_size=1, epochs=1)
    # Create the testing data set with scaled data.
    test_data = scaled_data[training_data_len - 60:, :]
    # Create the data sets x_test and y_test to test the prediction capability of the model.
    x_test = []
    # y_test will hold the actual values for the stock market days we are trying to predict.
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])
    # Convert the data to a numpy array
    x_test = np.array(x_test)
    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    # Get the models predictions
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    # Get the r2 value to evaluate the accuracy of the model.
    accuracy = r2_score(y_test, predictions)
    st.write(f"R2 score of this model is {accuracy:.2f}")
    # Plot the data. This plot shows predicted vs. actual closing price for the selected stock.
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    data = valid.reset_index().melt('Date')
    data2 = data.rename(columns={"value": "Amount", "variable": "Measure"}, errors="raise")
    alt_chart = alt.Chart(data2).mark_line().encode(
        x='Date',
        y='Amount',
        color='Measure'
    ).properties(title=f"Predicted vs. Actual Closing Price for {name}", height=500, width=750).interactive()
    st.write(alt_chart)
    # Scatter plot for predicted vs close prices; this shows how close the model's predicted values aligned with
    # the actual closing prices for the selected stock. A 45-degree angle would mean the model perfectly predicted
    # the closing price.
    scatter = alt.Chart(valid).mark_circle(size=60).encode(
        alt.X('Close',
              scale=alt.Scale(zero=False)
              ),
        alt.Y('Predictions',
              scale=alt.Scale(zero=False)
              )
    ).properties(title=f"Predicted vs. Actual Closing Price for {name}", height=450, width=670).interactive()
    st.write(scatter)
    # Histogram chart showing the distribution of errors in terms of % for predicted vs. actual stock prices.
    valid['Error $'] = valid['Predictions'] - valid['Close']
    valid['Error %'] = valid['Error $'] / valid['Close']
    valid['Error %'] = valid['Error %'] * 100
    histogram = alt.Chart(valid).mark_bar().encode(
        alt.X("Error %", bin=True),
        y='count()',
    ).properties(title=f"Predicted price error for {name}", height=450, width=670).interactive()
    st.write(histogram)
    # Predict the next day's closing price
    # Get the quote
    stock_data = get_stock_data(ticker, start, end)
    new_df = stock_data.filter(['Close'])
    # Get the last 60 days closing price and convert the dataframe to an array
    last_60_days = new_df[-60:].values
    # Scale the data to be values between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    # Create a list with the last 60 days.
    X_test = [last_60_days_scaled]
    # Convert to numpy array
    X_test = np.array(X_test)
    # Reshape the data
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    # Get predicted scaled price
    predicted_price = model.predict(X_test)
    # Undo the scaling
    predicted_price = scaler.inverse_transform(predicted_price)
    # Get last predicted value
    length = len(valid)
    prediction_values = valid['Predictions']
    last_day = prediction_values.iloc[length - 1]
    predicted_price_value = predicted_price.item(0)
    # Check if predicted value went up or down. If predicted price is higher, recommend buying the stock.
    # If the predicted price is lower, recommend selling the stock.
    if last_day < predicted_price:
        st.write(f"Predicted stock price for {name} tomorrow is {predicted_price_value:.2f}. This is greater"
                 f" than the previous predicted price of {last_day:.2f}, therefore The Prophet "
                 f"recommends buying {name} stock.")
    else:
        st.write(f"Predicted stock price for {name} tomorrow is {predicted_price_value:.2f}. This is less"
                 f" than the previous predicted price of {last_day:.2f}, therefore The Prophet "
                 f"recommends selling {name} stock.")
