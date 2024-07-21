import fetch
import csv
import os
import pandas as pd


def inflation_points():
    fetch.get_inflation()
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


def inflation():
    fetch.get_inflation()
    data = []
    year = ""
    interest = 0
    inf = 0
    interest_change = 0
    inf_change = 0
    file = os.path.join(os.path.dirname(__file__), "Local", "inflationData.csv")
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 4):
            next(reader)
        for row in reader:
            if row[0][0:4] == "2023":
                if row[0][5:7] == "01":
                    year = row[0][0:4]
                    interest += float(row[1])
                    inf += float(row[3])
                    interest_change -= float(row[1])
                    inf_change -= float(row[3])
                elif row[0][5:7] == "06":
                    interest += float(row[1])
                    inf += float(row[3])
                    interest /= 12
                    inf /= 12
                    interest_change += float(row[1])
                    inf_change += float(row[3])
                    data.append([year, interest, inf, interest_change, inf_change])
                elif row[0][5:7] == "07":
                    continue
                else:
                    interest += float(row[1])
                    inf += float(row[3])
            else:
                if row[0][5:7] == "01":
                    year = row[0][0:4]
                    interest += float(row[1])
                    inf += float(row[3])
                    interest_change -= float(row[1])
                    inf_change -= float(row[3])
                elif row[0][5:7] == "12":
                    interest += float(row[1])
                    inf += float(row[3])
                    interest /= 12
                    inf /= 12
                    interest_change += float(row[1])
                    inf_change += float(row[3])
                    data.append([year, interest, inf, interest_change, inf_change])
                    interest = 0
                    inf = 0
                    interest_change = 0
                    inf_change = 0
                else:
                    interest += float(row[1])
                    inf += float(row[3])

        compiled = pd.DataFrame(data, columns=['Year', 'Average Interest Rate', 'Average Inflation Rate',
                                               'Year-In Interest Rate Change', 'Year-In Inflation Rate Change'])
        compiled.to_csv('inflation.csv', index=False)
        print("Inflation Complete")


if __name__ == "__main__":
    inflation()
    fetch.flush_local()
