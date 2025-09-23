import pandas as pd

def load_stock_data(file_path):
    # Reads CSV and sorts by Date
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.to_csv('saved_data_test.csv')
    
    df.sort_values('Date', inplace=True)
    return df