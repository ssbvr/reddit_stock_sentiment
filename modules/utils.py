from datetime import datetime

def get_date_windows(start_date, end_date):
    """
    Determine which time windows the date range covers.
    """
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Calculate the difference between the end date and the start date
    date_diff = (end_date - start_date).days

    # Define the date windows and their lengths in days
    date_windows = {
        'day': 0,
        'week': 1,
        'month': 7,
        'year': 30,
        'all': 365
    }

    # Determine which windows the date range covers
    windows_covered = [window for window, length in date_windows.items() if date_diff >= length]

    return windows_covered