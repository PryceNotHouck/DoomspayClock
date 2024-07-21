import csv
import os
import pandas as pd


def sort_annual():
    for year in range(1929, 2023):
        data = []
        columns = []
        annual_data_path = os.path.join(os.path.dirname(__file__), "Annual Data")
        for file in os.listdir(annual_data_path):
            file_path = os.path.join(os.path.dirname(__file__), "Annual Data", file)
            print(file_path)
            with open(file_path,  newline='') as f:
                reader = csv.reader(f)
                set_columns = False
                for row in reader:
                    if not set_columns:
                        row.reverse()
                        row.pop()
                        row.reverse()
                        columns += row
                        set_columns = True
                        check_next = reader.__next__()
                        if int(check_next[0]) > year:
                            for i in range(len(row)):
                                data.append(0.0)
                            break
                        else:
                            check_next.reverse()
                            check_next.pop()
                            check_next.reverse()
                            for i in range(0, len(check_next)):
                                try:
                                    converted = float(check_next[i])
                                    check_next[i] = converted
                                except ValueError:
                                    check_next[i] = 0.0
                            data += check_next
                        continue
                    if int(row[0]) != year:
                        continue
                    else:
                        row.reverse()
                        row.pop()
                        row.reverse()
                        for i in range(0, len(row)):
                            try:
                                converted = float(row[i])
                                row[i] = converted
                            except ValueError:
                                row[i] = 0.0
                        data += row


if __name__ == '__main__':
    sort_annual()
