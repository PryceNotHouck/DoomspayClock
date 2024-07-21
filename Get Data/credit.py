import fetch
import csv
import os
import pandas as pd


def credit_points():
    fetch.get_credit()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local")

    for file in os.listdir(local_path):
        file_path = os.path.join(os.path.dirname(__file__), "Local", file)
        if file_path.endswith("BEA"):
            continue
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for i in range(0, 11):
                next(reader)
            for row in reader:
                points += len(row)
    #fetch.flush_local()
    return points


def credit():
    fetch.get_credit()
    data = {}
    year = ""
    bus_del = 0
    delta_bus_del = 0
    all_del = 0
    delta_all_del = 0
    credit_del = 0
    delta_credit_del = 0
    file1 = os.path.join(os.path.dirname(__file__), "Local", "DRCLACBS.csv")
    file2 = os.path.join(os.path.dirname(__file__), "Local", "DRALACBN.csv")
    file3 = os.path.join(os.path.dirname(__file__), "Local", "DRCCLACBS.csv")

    with open(file1, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 11):
            next(reader)
        for row in reader:
            if row[0][0:4] == "2024":
                data.setdefault("2024", [2.68, 0, 0, 0.07, 0, 0])
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
                        data[year][3] = delta_bus_del
                    else:
                        data[year] = [bus_del, 0, 0, delta_bus_del, 0, 0]
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
                    data["2024"][4] = 0.02
                else:
                    data["2024"] = [0, 1.44, 0, 0, 0.02, 0]
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
                        data[year][4] = delta_all_del
                    else:
                        data[year] = [0, all_del, 0, 0, delta_all_del, 0]
                    all_del = 0
                    delta_all_del = 0
                else:
                    all_del += float(row[1])

        with open(file3, newline='') as f:
            reader = csv.reader(f)
            for i in range(0, 11):
                next(reader)
            for row in reader:
                if row[0][0:4] == "2024":
                    if "2024" in data:
                        data["2024"][2] = 3.16
                        data["2024"][5] = 0.08
                    else:
                        data["2024"] = [0, 0, 3.16, 0, 0, 0.08]
                else:
                    if row[0][5:7] == "01":
                        year = row[0][0:4]
                        credit_del += float(row[1])
                        delta_credit_del -= float(row[1])
                    elif row[0][5:7] == "10":
                        credit_del += float(row[1])
                        credit_del /= 4
                        delta_credit_del += float(row[1])
                        if year in data:
                            data[year][2] = credit_del
                            data[year][5] = delta_credit_del
                        else:
                            data[year] = [0, 0, credit_del, 0, 0, delta_credit_del]
                        credit_del = 0
                        delta_credit_del = 0
                    else:
                        credit_del += float(row[1])

    data_list = [[year, *values] for year, values in sorted(data.items())]
    compiled = pd.DataFrame(data_list, columns=['Year', 'Average Consumer Loan Default Rate',
                                                'Average All Loans Default Rate', 'Average Credit Delinquency',
                                                'Year-In Consumer Loan Default Change',
                                                'Year-In All Loans Default Change',
                                                'Year-In Credit Delinquency Rate Change'])
    compiled.to_csv('credit.csv', index=False)
    print("Credit Delinquency Complete")


if __name__ == "__main__":
    print("Credit Delinquency Data Points:", f'{credit_points():,}')
