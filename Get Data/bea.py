import fetch
import csv
import os
import pandas as pd


def gdp_points():
    # fetch.fetch_bea()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local/BEA")
    for year in os.listdir(local_path):
        if year == "2024":
            continue
        year_path = os.path.join(local_path, year)
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            for file in os.listdir(quarter_path):
                if file.startswith("Section1"):
                    file_path = os.path.join(quarter_path, file)
                    with open(file_path, newline='') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            points += len(row)
                elif file.startswith("Section2"):
                    file_path = os.path.join(quarter_path, file)
                    with open(file_path, newline='') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            points += len(row)
                else:
                    continue
    return points


def trade_points():
    # fetch.fetch_bea()
    points = 0
    local_path = os.path.join(os.path.dirname(__file__), "Local/BEA")
    for year in os.listdir(local_path):
        if year == "2024":
            continue
        year_path = os.path.join(local_path, year)
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            for file in os.listdir(quarter_path):
                if file.startswith("Section4"):
                    file_path = os.path.join(quarter_path, file)
                    with open(file_path, newline='') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            points += len(row)
                elif file.startswith("Section5"):
                    file_path = os.path.join(quarter_path, file)
                    with open(file_path, newline='') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            points += len(row)
                else:
                    continue
    return points


def process0(file, data):
    return data


def process1(file, data):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        row = []
        exit_table = False
        years = []
        while not exit_table:
            try:
                if row[1].startswith('    Gross domestic product'):
                    exit_table = True
                else:
                    years = row
                    row = reader.__next__()
            except IndexError:
                row = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for i in range(0, len(years)):
            if years[i].endswith(".0"):
                years[i] = years[i][:-2]
        for year in years:
            try:
                test = data[year]
                data[year].append([])
            except KeyError:
                data[year] = []
        row.reverse()
        for j in range(0, 3):
            row.pop()
        row.reverse()
        for point in range(0, len(row)):
            # Gross Domestic Product Delta
            data[years[point]].append([row[point], file[64:68], file[69:71], 'GDP'])

        exit_table = False
        while not exit_table:
            row = reader.__next__()
            if row[1].startswith("Personal consumption expenditures"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'PCE'])
            elif row[1].startswith("Gross private domestic investment"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'GPDI'])
            elif row[1].startswith("Net exports of goods and services"):
                row = reader.__next__()
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'NE'])
            elif row[1].startswith("Government consumption expenditures and gross investment"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'GCEGI'])
                exit_table = True
    return data


def process2(file, data):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        row = []
        exit_table = False
        years = []
        while not exit_table:
            try:
                if row[1].startswith('Personal income'):
                    exit_table = True
                else:
                    years = row
                    row = reader.__next__()
            except IndexError:
                row = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for i in range(0, len(years)):
            if years[i].endswith(".0"):
                years[i] = years[i][:-2]
        for year in years:
            try:
                test = data[year]
                data[year].append([])
            except KeyError:
                data[year] = []
        exit_table = False
        while not exit_table:
            row = reader.__next__()
            if row[1].startswith("  Personal saving as a percentage of disposable personal income"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'PSPDPI'])
            elif row[1].startswith("    Disposable personal income, current dollars"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'DPI'])
                exit_table = True

        exit_table = False
        years = []
        while not exit_table:
            try:
                if row[1].startswith('    Personal consumption expenditures'):
                    exit_table = True
                else:
                    years = row
                    row = reader.__next__()
            except IndexError:
                row = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for i in range(0, len(years)):
            if years[i].endswith(".0"):
                years[i] = years[i][:-2]
        for year in years:
            try:
                test = data[year]
                data[year].append([])
            except KeyError:
                data[year] = []

        exit_table = False
        while not exit_table:
            row = reader.__next__()
            if row[1].startswith("Durable goods") or row[1].startswith("Goods"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'G'])
            elif row[1].startswith("Services"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'S'])
                exit_table = True
    return data


def process3(file, data):
    return data


def process4(file, data):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        row = []
        exit_table = False
        years = []
        while not exit_table:
            try:
                if row[1].startswith('    Exports of goods and services'):
                    exit_table = True
                else:
                    years = row
                    row = reader.__next__()
            except IndexError:
                row = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for i in range(0, len(years)):
            if years[i].endswith(".0"):
                years[i] = years[i][:-2]
        for year in years:
            try:
                test = data[year]
                data[year].append([])
            except KeyError:
                data[year] = []
        exit_table = False
        while not exit_table:
            row = reader.__next__()
            if row[1].startswith("Exports of goods"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'EG'])
            elif row[1].startswith("Exports of services"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'ES'])
            elif row[1].startswith("Imports of goods"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'IG'])
            elif row[1].startswith("Imports of services"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'IS'])
                exit_table = True
    return data


def process5(file, data):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        row = []
        exit_table = False
        years = []
        while not exit_table:
            try:
                if row[1].startswith('    Private fixed investment'):
                    exit_table = True
                else:
                    years = row
                    row = reader.__next__()
            except IndexError:
                row = reader.__next__()
        years.remove("Line")
        years.remove("")
        years.remove("")
        for i in range(0, len(years)):
            if years[i].endswith(".0"):
                years[i] = years[i][:-2]
        for year in years:
            try:
                test = data[year]
                data[year].append([])
            except KeyError:
                data[year] = []
        exit_table = False
        while not exit_table:
            row = reader.__next__()
            if row[1].startswith("Nonresidential"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'NRES'])
            elif row[1].startswith("  Equipment and software"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'EQSW'])
            elif row[1].startswith("Residential"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'RES'])
            elif row[1].startswith("  Equipment"):
                row.reverse()
                for j in range(0, 3):
                    row.pop()
                row.reverse()
                for point in range(0, len(row)):
                    data[years[point]].append([row[point], file[64:68], file[69:71], 'EQP'])
                exit_table = True
    return data


def process6(file, data):
    return data


def process7(file, data):
    return data


def process8(file, data):
    return data


def gdp():
    #fetch.fetch_bea()
    data = {}
    local_path = os.path.join(os.path.dirname(__file__), "Local/BEA")

    for year in os.listdir(local_path):
        if year == "2024":
            continue
        year_path = os.path.join(local_path, year)
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            for file in os.listdir(quarter_path):
                if file.startswith("Section1"):
                    file_path = os.path.join(quarter_path, file)
                    data = process1(file_path, data)
                elif file.startswith("Section2"):
                    file_path = os.path.join(quarter_path, file)
                    data = process2(file_path, data)
                else:
                    continue

    years = data.keys()
    intermediate = []
    final = []
    for year in sorted(years):
        intermediate.append([year] + data[year])
        final.append([year] + [-1])
    for i in range(0, len(intermediate)):
        seen = ["Year", "Last Reference Year"]
        for var in intermediate[i]:
            if var == final[i][0]:
                continue
            try:
                if var[3] in seen:
                    if int(var[1]) > final[i][1]:
                        final[i][1] = int(var[1])
                        final[i][seen.index(var[3])] = var[0]
                else:
                    seen.append(var[3])
                    final[i][1] = int(var[1])
                    final[i].append(var[0])
            except IndexError:
                continue
    compiled = pd.DataFrame(final, columns=["Year", "Last Reference Year", "GDP Delta",
                                            "Personal Consumption Expenditures", "Gross Private Domestic Investment",
                                            "Net Exports", "Government Consumption and Gross Investment",
                                            "Personal Savings %", "Disposable Personal Income",
                                            "Goods Consumption", "Service Consumption"])
    compiled.to_csv('gdp.csv', index=False)
    print("GDP Complete")


def trade():
    # fetch.fetch_bea()
    data = {}
    local_path = os.path.join(os.path.dirname(__file__), "Local/BEA")

    for year in os.listdir(local_path):
        if year == "2024":
            continue
        year_path = os.path.join(local_path, year)
        for quarter in os.listdir(year_path):
            quarter_path = os.path.join(year_path, quarter)
            for file in os.listdir(quarter_path):
                if file.startswith("Section4"):
                    file_path = os.path.join(quarter_path, file)
                    data = process4(file_path, data)
                elif file.startswith("Section5"):
                    file_path = os.path.join(quarter_path, file)
                    data = process5(file_path, data)
                else:
                    continue

    years = data.keys()
    intermediate = []
    final = []
    for year in sorted(years):
        intermediate.append([year] + data[year])
        final.append([year] + [-1])
    for i in range(0, len(intermediate)):
        seen = ["Year", "Last Reference Year"]
        for var in intermediate[i]:
            if var == final[i][0]:
                continue
            try:
                if var[3] in seen:
                    if int(var[1]) > final[i][1]:
                        final[i][1] = int(var[1])
                        final[i][seen.index(var[3])] = var[0]
                else:
                    seen.append(var[3])
                    final[i][1] = int(var[1])
                    final[i].append(var[0])
            except IndexError:
                continue
    compiled = pd.DataFrame(final, columns=["Year", "Last Reference Year", "Export of Goods", "Export of Services",
                                            "Import of Goods", "Export of Goods", "Nonresidential",
                                            "Equipment and Software", "Residential", "Equipment"])
    compiled.to_csv('trade.csv', index=False)
    print("Trade/Foreign Complete")


if __name__ == "__main__":
    trade()
