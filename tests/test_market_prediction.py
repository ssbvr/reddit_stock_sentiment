import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from modules.market_prediction import (
    calculate_trend,
    calculate_trend_reversals,
    map_sentiment_scores,
    predict_market_behavior,
)
import numpy as np


@pytest.fixture
def stock_data():
    """
    Generate mock stock data for testing
    """
    data = {
        "Close": [1, 2, 3, 4, 5],
        "moving_average": [1.0, 1.5, 2.0, 2.5, 3.0],
        "trend": [1, 1, 1, 1, 1],
        "prev_trend": [np.nan, 1, 1, 1, 1],
        "trend_reversal": [np.nan, 0, 0, 0, 0],
    }
    index = pd.date_range(start="2020-01-01", periods=5)
    return pd.DataFrame(data, index=index)


@pytest.fixture
def sentiment_scores():
    """
    Generate mock sentiment scores for testing
    """
    scores = {
        "day": {"AAPL": {"compound": 0.2}},
        "week": {"AAPL": {"compound": 0.3}},
        "month": {"AAPL": {"compound": 0.4}},
        "year": {"AAPL": {"compound": 0.5}},
        "all": {"AAPL": {"compound": 0.6}},
    }
    return scores


# Now you can start to write tests for your functions
def test_calculate_trend(stock_data):
    trend = calculate_trend(stock_data)
    assert (trend == stock_data["trend"]).all()


def test_calculate_trend_reversals(stock_data):
    trend_reversal = calculate_trend_reversals(stock_data)
    assert (trend_reversal == stock_data["trend_reversal"]).all()


def test_map_sentiment_scores(stock_data, sentiment_scores):
    stock_data_mapped = map_sentiment_scores(stock_data, sentiment_scores, "AAPL")
    assert "sentiment" in stock_data_mapped.columns


# Mocking the yfinance library and LogisticRegression
@patch("yfinance.download")
@patch("sklearn.linear_model.LogisticRegression")
def test_predict_market_behavior(mock_LR, mock_download, stock_data, sentiment_scores):
    # Setup your mocks
    mock_download.return_value = stock_data

    # Create two mock models for the two instances of LogisticRegression
    mock_model_1 = MagicMock()
    mock_model_2 = MagicMock()
    mock_model_1.fit.return_value = None
    mock_model_1.score.return_value = 1.0
    mock_model_1.predict.return_value = [0]
    mock_model_2.fit.return_value = None
    mock_model_2.score.return_value = 1.0
    mock_model_2.predict.return_value = [0]

    # Set the side_effect of mock_LR to return a different mock model for each call
    mock_LR.side_effect = [mock_model_1, mock_model_2]

    # Run your function with the mocks
    predict_market_behavior("AAPL", sentiment_scores, "2020-01-01", "2020-01-05")

    # Assert that your mocks were called as expected
    mock_download.assert_called_once_with("AAPL", start="2020-01-01", end="2020-01-05")
    assert (
        mock_LR.call_count == 2
    )  # Expect two instances of LogisticRegression to be created
    assert (
        mock_model_1.fit.call_count == 1
    )  # Check if fit is called once on the mock_model_1
    assert (
        mock_model_2.fit.call_count == 1
    )  # Check if fit is called once on the mock_model_2
