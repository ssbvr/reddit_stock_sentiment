import matplotlib.pyplot as plt
import pandas as pd

def plot_data(stock_data, ticker, start_date=None, end_date=None, prediction=None):
    plt.figure(figsize=(14,10))
    
    # If start_date and end_date were provided, select this range in the data
    if start_date and end_date:
        stock_data = stock_data.loc[start_date:end_date]

    # Plot stock closing price
    plt.subplot(411)
    stock_data['Close'].plot(label='Closing price', color='blue')
    plt.axvspan(stock_data.index[-2], stock_data.index[-1], facecolor='gray', alpha=0.5)
    plt.ylabel('Price ($)')
    plt.title(f'{ticker} Stock Data')
    plt.legend()

    # Plot trend
    plt.subplot(412)
    stock_data['prev_trend'].plot(label='Previous traiding day trend (5 day moving average)', color='red')
    plt.axvspan(stock_data.index[-2], stock_data.index[-1], facecolor='gray', alpha=0.5)
    plt.legend()

    # Plot sentiment scores
    plt.subplot(413)
    stock_data['sentiment'].plot(label='Sentiment score', color='orange')
    plt.axvspan(stock_data.index[-2], stock_data.index[-1], facecolor='gray', alpha=0.5)
    plt.legend()

    # Plot trend reversals
    plt.subplot(414)
    stock_data['trend_reversal'].plot(label='Trend reversal', color='green')
    plt.axvspan(stock_data.index[-2], stock_data.index[-1], facecolor='gray', alpha=0.5)
    if prediction is not None:
        plt.scatter(stock_data.index[-1], prediction, color='red', zorder=5)
    plt.legend()

    plt.tight_layout()
    plt.show()


