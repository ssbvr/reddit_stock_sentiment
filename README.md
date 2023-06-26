# Reddit Stock Sentiment Analysis

This project provides a tool to perform sentiment analysis on Reddit's r/wallstreetbets subreddit and to predict today's market behavior. The application uses Reddit's API to extract relevant posts and comments, applies sentiment analysis using the NLTK Vader model, and leverage this data to predict stock market behavior.

## Table of Contents

0. [Disclaimer](#disclaimer)
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Testing](#testing)
5. [Contributing](#contributing)

## Disclamer

This project, its code, and its outputs are provided for informational purposes only. The information should not be interpreted as any form of investment advice, financial advice, trading advice, or recommendation. We do not advise or recommend that you buy, sell, or hold any security, cryptocurrency, or any other investment product or make any particular investment strategy.

Before making financial decisions, please consult with a certified financial advisor or do your own research and analysis. The authors and all those associated with this project are not responsible for any potential losses, damages, or consequences that may result from the use of the data, code, or interpretations provided here. Please invest responsibly.

## Features

- Reddit Data Extraction: Extracts top posts and comments from r/wallstreetbets subreddit using Reddit's API.
- Data Processing: Identifies stock tickers to posts and comments.
- Sentiment Analysis: Applies sentiment analysis on the extracted text data using the NLTK Vader model.
- Market Prediction: Combines the results from the sentiment analysis with other finanncial data to predict market behaviors.

## Installation

To install the application, follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/ssbvr/reddit_stock_sentiment.git
cd reddit_stock_sentiment
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```
If you plan to run the jupyter notebooks, you will also need to install the jupyter package:
```bash
pip install jupyter
```
3. Create a .env file in the root directory and add your Reddit API and working directory:
```makefile
REDDIT_CLIENT_ID=<your_reddit_client_id>
REDDIT_SECRET=<your_reddit_secret>
REDDIT_USER_AGENT=<your_reddit_user_agent>
WORK_DIR=<your_working_directory>
```

## Usage

To run the application, use the main.py script:
```bash
python main.py
```
The application will extract data from the subreddit, apply sentiment analysis, and predict market behaviors of the stocks discussed today on r/wallstreetbets.

## Testing

This application includes unit tests. To run them, use the following command:
```bash
pytest
```

## Contributing

Contributions to this project are welcome. Please fork the repository, create your feature branch, commit your changes, and create a new Pull Request.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License.