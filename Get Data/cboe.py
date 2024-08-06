# Used here: W3 schools guide for Pandas Dataframes.

import fetch
import csv
import os
import pandas as pd


def cboe_points():
    fetch.get_cboe()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local")

    for file in os.listdir(local_path):
        file_path = os.path.join(os.path.dirname(__file__), "Local", file)
        if file_path.endswith("BEA"):
            continue
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                points += len(row)
    #fetch.flush_local()
    return points


def cboe():
    fetch.get_cboe()
    data = {}
    gold = os.path.join(os.path.dirname(__file__), "Local", "GVZ_History.csv")
    oil = os.path.join(os.path.dirname(__file__), "Local", "OVX_History.csv")
    nine_day = os.path.join(os.path.dirname(__file__), "Local", "VIXS&P9D_History.csv")
    vvix = os.path.join(os.path.dirname(__file__), "Local", "VVIX_History.csv")
    apple = os.path.join(os.path.dirname(__file__), "Local", "VXAPL_History.csv")
    amazon = os.path.join(os.path.dirname(__file__), "Local", "VXAZN_History.csv")
    emvix = os.path.join(os.path.dirname(__file__), "Local", "VXEEM_History.csv")

    def update_data(year, index_avg, index_delta, avg_value, delta_value):
        if year not in data:
            data[year] = [0] * 14
        data[year][index_avg] = avg_value
        data[year][index_delta] = delta_value

    def process_file(filename, avg_index, delta_index, start_year, end_year, start_month):
        points = 0
        avg_value = 0
        first_value = 0
        last_value = 0
        year = ""
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                row_year = row[0][6:10]
                if start_year <= row_year < end_year:
                    if row[0][0:2] == start_month:
                        year = row_year
                        avg_value += float(row[1])
                        first_value = float(row[1])
                        points += 1
                    elif row[0][0:2] == '12':
                        avg_value += float(row[1])
                        last_value = float(row[1])
                        points += 1
                        avg_value /= points
                        delta_value = last_value - first_value
                        update_data(year, avg_index, delta_index, avg_value, delta_value)
                        avg_value = 0
                        first_value = 0
                        last_value = 0
                        points = 0
                    else:
                        avg_value += float(row[1])
                        points += 1
                else:
                    if row[0][0:2] == '01':
                        year = row_year
                        avg_value += float(row[1])
                        first_value = float(row[1])
                        points += 1
                    elif row[0][0:2] == '07':
                        avg_value += float(row[1])
                        last_value = float(row[1])
                        points += 1
                        avg_value /= points
                        delta_value = last_value - first_value
                        update_data(year, avg_index, delta_index, avg_value, delta_value)
                        avg_value = 0
                        first_value = 0
                        last_value = 0
                        points = 0
                    else:
                        avg_value += float(row[1])
                        points += 1

    process_file(gold, 0, 7, '2009', '2024', '09')
    process_file(oil, 1, 8, '2009', '2024', '09')
    process_file(nine_day, 2, 9, '2011', '2024', '01')
    process_file(vvix, 3, 10, '2006', '2024', '03')
    process_file(apple, 4, 11, '2011', '2024', '01')
    process_file(amazon, 5, 12, '2011', '2024', '01')
    process_file(emvix, 6, 13, '2011', '2024', '03')

    years = data.keys()
    averages = ["Gold Average", "Oil Average", "S&P 500 9-Day Average", "VVIX Average", "Apple Average", "Amazon Average", "EMVIX Average"]
    deltas = ["Gold Delta", "Oil Delta", "S&P 500 9-Day Delta", "VVIX Delta", "Apple Delta", "Amazon Delta", "EMVIX Delta"]
    table = []

    for year in sorted(years):
        table.append([year] + data[year])

    compiled = pd.DataFrame(table, columns=["Year"] + averages + deltas)
    compiled.to_csv('cboe.csv', index=False)
    print("CBOE Complete")


if __name__ == "__main__":
    cboe()
    fetch.flush_local()
