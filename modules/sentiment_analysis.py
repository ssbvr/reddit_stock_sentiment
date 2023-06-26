import os
import json
import nltk
from prettytable import PrettyTable
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import WORK_DIR
from modules.data_processing import load_processed_data

nltk.download("vader_lexicon")


def analyze_sentiment_nltk(comments):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = []
    for comment in comments:
        sentiment.append(analyzer.polarity_scores(comment))

    return sentiment


def perform_sentiment_analysis_nltk(file_path, windows=["day"]):
    for window in windows:
        ticker_comments = load_processed_data(
            file_path.replace(".json", f"_{window}.json")
        )

        sentiment_data = {}
        for ticker in ticker_comments:
            sentiment_data[ticker] = analyze_sentiment_nltk(ticker_comments[ticker])

        with open(
            os.path.join(WORK_DIR, f"data/sentiment_scores_{window}.json"), "w"
        ) as file:
            json.dump(sentiment_data, file, indent=4)


def average_sentiment_scores(sentiment_scores_file, windows=["day"]):
    avg_sentiment_scores = {}
    for window in windows:
        sentiment_scores_file_tmp = sentiment_scores_file.replace(
            ".json", f"_{window}.json"
        )
        with open(sentiment_scores_file_tmp, "r") as file:
            sentiment_scores = json.load(file)

        avg_sentiment_scores[window] = {}
        for ticker, scores in sentiment_scores.items():
            avg_scores = {"neg": 0, "neu": 0, "pos": 0, "compound": 0}
            for score in scores:
                avg_scores["neg"] += score["neg"]
                avg_scores["neu"] += score["neu"]
                avg_scores["pos"] += score["pos"]
                avg_scores["compound"] += score["compound"]

            num_scores = len(scores)
            avg_scores = {key: val / num_scores for key, val in avg_scores.items()}
            avg_scores["count"] = num_scores
            avg_sentiment_scores[window][ticker] = avg_scores

    return avg_sentiment_scores


def print_sentiment_table(avg_sentiment_scores, windows=["day"]):
    # Loop over avg_sentiment_scores dictionary and add rows to the table
    for window in windows:
        print(f"============================== {window} ==============================")
        # Define table and its column names
        table = PrettyTable(
            ["Ticker", "Negative", "Neutral", "Positive", "Compound", "# Comments"]
        )
        for ticker, scores in avg_sentiment_scores[window].items():
            table.add_row(
                [
                    ticker,
                    round(scores["neg"], 4),
                    round(scores["neu"], 4),
                    round(scores["pos"], 4),
                    round(scores["compound"], 4),
                    scores["count"],
                ]
            )
        # Print the table
        print(table)
        print("")
