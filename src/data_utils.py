import pandas as pd

def load_data():
    df = pd.read_csv("freelancer_earnings_bd.xls")
    return df
