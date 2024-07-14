import requests
import csv
import openpyxl
import os


def flush_local():
    dir_path = os.path.join(os.path.dirname(__file__), "Local")
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


def convert_xlsx(file):
    file_path = "Local/" + str(file)
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    csv_file_path = os.path.splitext(file_path)[0] + ".csv"
    with open(csv_file_path, 'w', newline="") as csvfile:
        col = csv.writer(csvfile)
        for row in sheet.iter_rows(values_only=True):
            col.writerow(row)

    os.remove(file_path)


def fetch(var, file):
    url = "https://raw.githubusercontent.com/PryceNotHouck/DoomspayClock/master/Datasets/"
    match var:
        case 0:
            # GDP Growth
            pass
        case 1:
            # Inflation Rate
            pass
        case 2:
            # Trade/Foreign Investment
            pass
        case 3:
            # Consumer Price Index
            pass
        case 4:
            # Unemployment
            url += "BLS/" + file
        case 5:
            # Housing Prices
            pass
        case 6:
            # Loan Default Rates
            pass
        case 7:
            # Credit Delinquency
            pass
        case 8:
            # Gold ETF
            pass
        case 9:
            # Oil ETF
            pass
        case 10:
            # S&P 500 9-Day
            pass
        case 11:
            # VIX Index
            pass
        case 12:
            # VIX Emerging Markets
            pass
        case 13:
            # VIX Apple
            pass
        case 14:
            # VIX Amazon
            pass

    res = requests.get(url, allow_redirects=True)
    file_path = "Local/" + file
    if file.endswith(".xlsx"):
        with open(file_path, 'wb') as f:
            f.write(res.content)
        convert_xlsx(file)


if __name__ == "__main__":
    fetch(4, "laucnty00.xlsx")
    flush_local()
