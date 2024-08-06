# Used here: W3 schools guide for Pandas Dataframes.

import fetch
import csv
import os
import pandas as pd


def cpi_points():
    fetch.get_cpi()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local")

    for file in os.listdir(local_path):
        file_path = os.path.join(os.path.dirname(__file__), "Local", file)
        if file_path.endswith("BEA"):
            continue
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for i in range(0, 4):
                next(reader)
            for row in reader:
                points += len(row)
    #fetch.flush_local()
    return points


def cpi():
    fetch.get_cpi()
    data = []
    year = ""
    confidence = 0
    confidence_delta = 0
    file = os.path.join(os.path.dirname(__file__), "Local", "cpi_data.csv")
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 4):
            next(reader)
        for row in reader:
            if int(row[0][-2:]) >= 92:
                year = "19" + row[0][-2:]
            else:
                year = "20" + row[0][-2:]
            confidence = float(row[1])
            if confidence_delta != 0:
                confidence_delta -= confidence
                confidence_delta *= -1
            data.append([year, confidence, confidence_delta])
            confidence_delta = confidence
    compiled = pd.DataFrame(data, columns=['Year', 'Consumer Confidence', 'Consumer Confidence Delta'])
    compiled.to_csv('cpi.csv', index=False)
    print("CPI Complete")


if __name__ == "__main__":
    cpi()
    fetch.flush_local()
