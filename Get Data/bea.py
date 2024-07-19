import fetch
import csv
import os
import pandas as pd


def gdp_points():
    return 0


def process0(file, data):
    return 0


def process1(file, data):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for i in range(0, 131):
            next(reader)
        years = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for year in years:
            # Adjacency List - Year : Array[[Data Point, Year of Origin]]
            data[year] = []
        for i in range(1, 24):
            row = reader.__next__()
            row.reverse()
            for j in range(0, 3):
                row.pop()
            row.reverse()
            if i == 1 or i == 2 or i == 6 or i == 14 or i == 17 or i == 20:
                # 1 - GDP Delta
                # 2 - Delta Personal Consumption Expenditures
                # 6 - Delta Gross Private Domestic Investment
                # 14 - Delta Net Exports
                # 17 - Delta Net Imports
                # 20 - Government Consumption Expenditures and Gross Investment
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68]])
    return data


def process2(file, data):
    return 0


def process3(file, data):
    return 0


def process4(file, data):
    return 0


def process5(file, data):
    return 0


def process6(file, data):
    return 0


def process7(file, data):
    return data


def process8(file, data):
    return 0


def gdp():
    #fetch.fetch_bea()
    data = {}
    local_path = os.path.join(os.path.dirname(__file__), "Local/BEA")
    year = 2006

    for year in os.listdir(local_path):
        year_path = os.path.join(local_path, year)
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            for file in os.listdir(quarter_path):
                if file.startswith("Section1"):
                    file_path = os.path.join(quarter_path, file)
                    data = process1(file_path, data)
                elif file.startswith("Section7"):
                    file_path = os.path.join(quarter_path, file)
                    data = process7(file_path, data)
                else:
                    continue


if __name__ == "__main__":
    gdp()
