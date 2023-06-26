from unittest.mock import patch, mock_open
from modules.sentiment_analysis import analyze_sentiment_nltk, average_sentiment_scores


@patch("nltk.sentiment.vader.SentimentIntensityAnalyzer.polarity_scores")
def test_analyze_sentiment_nltk(mock_polarity_scores):
    mock_polarity_scores.return_value = {
        "neg": 0.0,
        "neu": 0.5,
        "pos": 0.5,
        "compound": 0.5,
    }
    comments = ["I love this stock!", "This stock is terrible!"]
    expected_output = [
        {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.5},
        {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.5},
    ]
    assert analyze_sentiment_nltk(comments) == expected_output


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"TSLA": [{"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.5}, {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.5}]}',
)
def test_average_sentiment_scores(mock_file):
    expected_output = {
        "day": {
            "TSLA": {"neg": 0.0, "neu": 0.5, "pos": 0.5, "compound": 0.5, "count": 2}
        }
    }
    assert average_sentiment_scores("dummy_path") == expected_output

