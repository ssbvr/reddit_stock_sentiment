from sklearn.model_selection import train_test_split
import sklearn.linear_model
import yfinance as yf
import pandas as pd
import numpy as np

def add_today_row(stock_data, end_date):
    if end_date in stock_data.index:
        raise ValueError("Stock data already contains today's date.")
    stock_data.loc[pd.to_datetime(end_date)] = [np.nan] * len(stock_data.columns)
    return stock_data


def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return add_today_row(stock_data, end_date)


def calculate_trend(data, window=5):
    """
    Calculate the trend based on a simple moving average.
    An upward trend is represented by 1 and a downward trend by 0.
    """
    # Calculate moving average
    data["moving_average"] = data["Close"].rolling(window=window).mean()

    # Calculate trend: 1 for upward trend and 0 for downward trend
    data["trend"] = (data["Close"] > data["moving_average"]).astype(int)
    
    # today has no stock closing price, so we set it to nan
    data.loc[data.index[-1], "trend"] = np.nan

    return data["trend"]


def calculate_trend_reversals(data):
    """
    Determine if there was a trend reversal.
    A trend reversal is represented by 1 and otherwise by 0.
    """
    # Shift the trend column to compare with the next day
    data["prev_trend"] = data["trend"].shift(1)

    # Calculate trend reversals: 1 for reversal and 0 for no reversal
    data["trend_reversal"] = (data["trend"] != data["prev_trend"]).astype(int)
    
    # todays has no stock closing price, so we set it to nan
    data.loc[data.index[-1], "trend_reversal"] = np.nan

    return data["trend_reversal"]


def map_sentiment_scores(stock_data, sentiment_scores, ticker):
    """
    Map sentiment scores to stock data based on date and aggregate sentiment scores according
    to the time windows "day", "week", "month", "year", "all".
    """
    sentiment_mapping = {}

    # Iterate over stock data dates
    for date in stock_data.index:
        # For each date, check which time window it falls into and assign the corresponding sentiment score
        if (
            date == stock_data.index[-1]
        ):  # The last date (most recent) gets the 'day' score
            if ticker in sentiment_scores["day"]:
                sentiment_mapping[date] = sentiment_scores["day"][ticker]["compound"]
            else:
                sentiment_mapping[date] = 0.0
        elif (
            stock_data.index[-1] - date
        ).days <= 7:  # Previous seven days get the 'week' score
            if ticker in sentiment_scores["week"]:
                sentiment_mapping[date] = sentiment_scores["week"][ticker]["compound"]
            else:
                sentiment_mapping[date] = 0.0
        elif (
            stock_data.index[-1] - date
        ).days <= 28:  # Previous three weeks get the 'month' score
            if ticker in sentiment_scores["month"]:
                sentiment_mapping[date] = sentiment_scores["month"][ticker]["compound"]
            else:
                sentiment_mapping[date] = 0.0
        elif (
            stock_data.index[-1] - date
        ).days <= 365:  # Previous eleven months get the 'year' score
            if ticker in sentiment_scores["year"]:
                sentiment_mapping[date] = sentiment_scores["year"][ticker]["compound"]
            else:
                sentiment_mapping[date] = 0.0
        else:  # All other days get the 'all' score
            if ticker in sentiment_scores["all"]:
                sentiment_mapping[date] = sentiment_scores["all"][ticker]["compound"]
            else:
                sentiment_mapping[date] = 0.0

    # Add a new 'sentiment' column to the stock data DataFrame
    stock_data["sentiment"] = pd.Series(sentiment_mapping)

    return stock_data


def predict_market_behavior(ticker, sentiment_scores, start_date, end_date):
    # Get stock data up to yesterday
    stock_data = get_stock_data(ticker, start_date, end_date)

    # Calculate trend and trend reversals
    stock_data["trend"] = calculate_trend(stock_data)
    stock_data["trend_reversal"] = calculate_trend_reversals(stock_data)

    # Add sentiment scores
    stock_data = map_sentiment_scores(stock_data, sentiment_scores, ticker)

    # Prepare data for model
    X = stock_data[["prev_trend", "sentiment"]]
    y = stock_data["trend_reversal"]
    
    # Remove first row because it has no previous trend
    # remove last row (today) because it has no trend reversal
    X_predict = X[-1:]
    X = X[1:-1]
    y = y[1:-1]
    
    # Split data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    # Train model
    model = sklearn.linear_model.LogisticRegression()
    model.fit(X_train, y_train)

    # Check model accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    # train model on all data except the last day
    model = sklearn.linear_model.LogisticRegression()
    model.fit(X, y)

    # predict trend reversal for the last day
    y_pred = model.predict(X_predict)
    if y_pred[0] == 0:
        print("Model prediction: No trend reversal.")
    else:
        print("Model prediction: trend reversal !!!")

    return model
