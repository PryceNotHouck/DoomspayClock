import fetch
import csv
import os
import pandas as pd


def loandefault_points():
    fetch.get_loan_default()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local")

    for file in os.listdir(local_path):
        file_path = os.path.join(os.path.dirname(__file__), "Local", file)
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for i in range(0, 11):
                next(reader)
            for row in reader:
                points += len(row)
    fetch.flush_local()
    print("Loan Default Data Points:", points)


def loandefault():
    fetch.get_loan_default()
    data = {}
    year = ""
    bus_del = 0
    delta_bus_del = 0
    all_del = 0
    delta_all_del = 0
    file1 = os.path.join(os.path.dirname(__file__), "Local", "DRBLACBS.csv")
    file2 = os.path.join(os.path.dirname(__file__), "Local", "DRALACBN.csv")

    with open(file1, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 11):
            next(reader)
        for row in reader:
            if row[0][0:4] == "2024":
                data.setdefault("2024", [1.13, 0, 0.10, 0])
            else:
                if row[0][5:7] == "01":
                    year = row[0][0:4]
                    bus_del += float(row[1])
                    delta_bus_del -= float(row[1])
                elif row[0][5:7] == "10":
                    bus_del += float(row[1])
                    bus_del /= 4
                    delta_bus_del += float(row[1])
                    if year in data:
                        data[year][0] = bus_del
                        data[year][2] = delta_bus_del
                    else:
                        data[year] = [bus_del, 0, delta_bus_del, 0]
                    bus_del = 0
                    delta_bus_del = 0
                else:
                    bus_del += float(row[1])

    with open(file2, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 11):
            next(reader)
        for row in reader:
            if row[0][0:4] == "2024":
                if "2024" in data:
                    data["2024"][1] = 1.44
                    data["2024"][3] = 0.02
                else:
                    data["2024"] = [0, 1.44, 0, 0.02]
            else:
                if row[0][5:7] == "01":
                    year = row[0][0:4]
                    all_del += float(row[1])
                    delta_all_del -= float(row[1])
                elif row[0][5:7] == "10":
                    all_del += float(row[1])
                    all_del /= 4
                    delta_all_del += float(row[1])
                    if year in data:
                        data[year][1] = all_del
                        data[year][3] = delta_all_del
                    else:
                        data[year] = [0, all_del, 0, delta_all_del]
                    all_del = 0
                    delta_all_del = 0
                else:
                    all_del += float(row[1])

    data_list = [[year, *values] for year, values in sorted(data.items())]
    compiled = pd.DataFrame(data_list, columns=['Year', 'Average Business Loan Default Rate',
                                                'Average All Loans Default Rate', 'Year-In Business Loan Default Change',
                                                'Year-In All Loans Default Change'])
    compiled.to_csv('loandefault.csv', index=False)
    print("Loan Default Complete")


if __name__ == "__main__":
    loandefault()
    fetch.flush_local()
