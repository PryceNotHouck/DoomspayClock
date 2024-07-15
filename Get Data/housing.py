import fetch
import pandas as pd
import os


def housing():
    fetch.get_housing()
    data = []
    file = os.path.join(os.path.dirname(__file__), "Local", "housingprices.csv")
    df = pd.read_csv(file, skiprows=6)

    # Idea for this one: Rows are 2000 - 2010, first column is year, second column is median price, third column is
    # change from Q1 of that year to Q4 (or last available quarter).


if __name__ == "__main__":
    housing()
    fetch.flush_local()