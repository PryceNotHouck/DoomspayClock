import requests
import csv
import openpyxl
import xlrd
import os
from datetime import datetime, timedelta


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


def convert_xls(file):
    file_path = "Local/" + str(file)
    csv_file_path = os.path.splitext(file_path)[0] + ".csv"
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    # Accounts for Excel's old base date (1900-01-01)
    base_date = datetime(1899, 12, 30)

    with open(csv_file_path, 'w', newline='') as csvfile:
        col = csv.writer(csvfile)
        for row in range(sheet.nrows):
            row_values = sheet.row_values(row)
            if isinstance(row_values[0], float):
                date_value = base_date + timedelta(days=row_values[0])
                row_values[0] = date_value.strftime("%Y-%m-%d")
            col.writerow(row_values)

    os.remove(file_path)


def fetch(var, file):
    print("Fetching:", file)
    url = "https://raw.githubusercontent.com/PryceNotHouck/DoomspayClock/master/Datasets/"
    match var:
        case 0:
            # GDP Growth
            pass
        case 1:
            # Inflation Rate, CPI
            url += "Statista/" + file
        case 2:
            # Trade/Foreign Investment
            pass
        case 3:
            # Unemployment
            url += "BLS/" + file
        case 4:
            # Housing Prices
            url += "FHFA/" + file
        case 5:
            # Loan Default Rates, Credit Delinquency
            url += "FRED/" + file
        case 6:
            # Cboe
            url += "Cboe/" + file

    res = requests.get(url, allow_redirects=True)
    file_path = "Local/" + file
    if file.endswith(".xlsx"):
        with open(file_path, 'wb') as f:
            f.write(res.content)
        convert_xlsx(file)
    elif file.endswith(".xls"):
        with open(file_path, 'wb') as f:
            f.write(res.content)
        convert_xls(file)
    else:
        with open(file_path, 'wb') as f:
            f.write(res.content)


def get_unemployment():
    year = -1
    for i in range(0, 24):
        year += 1
        file = "laucnty" + "{:02d}".format(year) + ".xlsx"
        fetch(3, file)
    year = 89
    for i in range(0, 10):
        year += 1
        file = "laucnty" + "{:02d}".format(year) + ".xlsx"
        fetch(3, file)


def get_inflation():
    fetch(1, "inflationData.xlsx")


def get_cpi():
    fetch(1, "cpi.xlsx")


def get_housing():
    fetch(4, "housingprices.xls")


def get_cboe():
    fetch(6, "GVZ_History.csv")
    fetch(6, "OVX_History.csv")
    fetch(6, "VIXS&P9D_History.csv")
    fetch(6, "VVIX_History.csv")
    fetch(6, "VXAPL_History.csv")
    fetch(6, "VXAZN_History.csv")
    fetch(6, "VXEEM_History.csv")


def get_loan_default():
    fetch(5, "DRBLACBS.xls")
    fetch(5, "DRALACBN.xls")


def get_credit():
    fetch(5, "DRALACBN.xls")
    fetch(5, "DRCLACBS.xls")
    fetch(5, "DRCCLACBS.xls")


if __name__ == "__main__":
    get_unemployment()
    flush_local()
