import os
from modules.reddit_data_extraction import (
    get_top_posts_and_comments,
    connect_to_reddit,
)
from modules.data_processing import load_tickers, process_data
from modules.sentiment_analysis import (
    perform_sentiment_analysis_nltk,
    average_sentiment_scores,
    print_sentiment_table,
)
from modules.market_prediction import predict_market_behavior
from config import WORK_DIR, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT
from modules.utils import get_date_windows
from datetime import datetime


def main(
    tickers_file_path,
    data_path,
    processed_data_path,
    sentiment_scores_path,
    start_date,
    end_date,
    post_limit,
    comment_limit,
):
    # Load tickers from file
    tickers = load_tickers(tickers_file_path)

    # Get date windows
    windows = get_date_windows(start_date, end_date)

    # Get top posts and comments from r/wallstreetbets
    reddit = connect_to_reddit(REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT)
    get_top_posts_and_comments(
        "wallstreetbets",
        reddit,
        data_path,
        windows=windows,
        post_limit=post_limit,
        comment_limit=comment_limit,
    )

    # Process Reddit data
    process_data(data_path, tickers_file_path, windows=windows)

    # Analyze sentiment and save scores to file
    perform_sentiment_analysis_nltk(processed_data_path, windows=windows)

    # print average sentiment scores
    avg_sentiment_scores = average_sentiment_scores(
        sentiment_scores_path, windows=windows
    )
    print_sentiment_table(avg_sentiment_scores, windows=windows)

    # Predict market behavior for each ticker
    for ticker in tickers:
        if ticker not in avg_sentiment_scores["day"].keys():
            continue
        print(
            f"Predicting market behavior for {ticker} "
            "based on today WallStreetBets subreddit sentiment score."
        )
        predict_market_behavior(ticker, avg_sentiment_scores, start_date, end_date)


if __name__ == "__main__":
    kwargs = dict(
        # Define paths to files
        tickers_file_path=os.path.join(WORK_DIR, "data/tickers.txt"),
        data_path=os.path.join(WORK_DIR, "data/top_posts_comments.json"),
        processed_data_path=os.path.join(
            WORK_DIR, "data/processed_top_posts_comments.json"
        ),
        sentiment_scores_path=os.path.join(WORK_DIR, "data/sentiment_scores.json"),
        # Define parameters
        start_date="2018-01-01",
        end_date=datetime.now().strftime("%Y-%m-%d"),  # Today's date
        post_limit=50,
        comment_limit=1000,
    )

    main(**kwargs)
