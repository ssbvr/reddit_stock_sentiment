import re
import json


def load_tickers(ticker_file_path):
    with open(ticker_file_path, "r") as file:
        return [line.strip() for line in file]


def process_data(file_path, ticker_file_path, windows=["day"]):
    for window in windows:
        file_path_tmp = file_path.replace(".json", f"_{window}.json")
        with open(file_path_tmp, "r") as file:
            post_comment_data = json.load(file)

        tickers = load_tickers(ticker_file_path)

        processed_data = []
        for post in post_comment_data:
            post["tickers"] = [
                ticker
                for ticker in tickers
                if re.search(r"\b" + ticker + r"\b", post["body"], re.I)
            ]

            for comment in post["comments"]:
                comment["tickers"] = [
                    ticker
                    for ticker in tickers
                    if re.search(r"\b" + ticker + r"\b", comment["body"], re.I)
                ]

            post["comments"] = [
                comment for comment in post["comments"] if any(comment["tickers"])
            ]

            # If post has at least one comment after filtering, include it in the processed data
            if post["comments"]:
                processed_data.append(post)

        with open(file_path_tmp.replace("/data/", "/data/processed_"), "w") as file:
            json.dump(processed_data, file, indent=4)


def load_processed_data(file_path):
    with open(file_path, "r") as file:
        processed_data = json.load(file)

    ticker_comment_dict = {}
    for post in processed_data:
        for comment in post["comments"]:
            for ticker in comment["tickers"]:
                if ticker not in ticker_comment_dict:
                    ticker_comment_dict[ticker] = [comment["body"]]
                else:
                    ticker_comment_dict[ticker].append(comment["body"])

    return ticker_comment_dict
