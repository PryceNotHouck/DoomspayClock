import fetch
import csv
import os
import pandas as pd


def housing():
    fetch.get_housing()
    data = []
    year = 0
    median = 0
    change = 0
    file = os.path.join(os.path.dirname(__file__), "Local", "housingprices.csv")
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 5):
            next(reader)
        for row in reader:
            if row[0] != 'US':
                break
            if row[1][2] == '1':
                if row[1][-1] == '1':
                    year = row[1][:4]
                    median += float(row[3])
                    change -= float(row[3])
                if row[1][-1] == '2':
                    median += float(row[3])
                    median /= 2
                    change += float(row[3])
                    data.append([year, median, change])
            else:
                if row[1][-1] == '1':
                    year = row[1][:4]
                    median += float(row[3])
                    change -= float(row[3])
                if row[1][-1] == '2' or row[1][-1] == '3':
                    median += float(row[3])
                if row[1][-1] == '4':
                    median += float(row[3])
                    median /= 4
                    change += float(row[3])
                    data.append([year, median, change])
                    year = 0
                    median = 0
                    change = 0
    fetch.flush_local()

    compiled = pd.DataFrame(data, columns=['Year', 'Average Median Price', 'Year-In Change'])
    compiled.to_csv('housing.csv', index=False)
    print("Housing Complete")


if __name__ == "__main__":
    housing()
    fetch.flush_local()