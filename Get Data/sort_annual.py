import csv
import os


def flush_years():
    dir_path = os.path.join(os.path.dirname(__file__), "Years")
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


def sort_annual():
    for year in range(1929, 2024):
        data = []
        data_columns = []
        annual_data_path = os.path.join(os.path.dirname(__file__), "Annual Data")
        for file in os.listdir(annual_data_path):
            file_path = os.path.join(os.path.dirname(__file__), "Annual Data", file)
            with open(file_path,  newline='') as f:
                reader = csv.reader(f)
                set_columns = False
                for row in reader:
                    if not set_columns:
                        row.remove(row[0])
                        data_columns += row
                        set_columns = True
                        check_next = reader.__next__()
                        if int(check_next[0]) > year:
                            for i in range(len(row)):
                                data.append(0.0)
                            break
                        else:
                            if int(check_next[0]) == year:
                                check_next.remove(check_next[0])
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
                        row.remove(row[0])
                        for i in range(0, len(row)):
                            try:
                                converted = float(row[i])
                                row[i] = converted
                            except ValueError:
                                row[i] = 0.0
                        data += row

        write_path = "Years/" + str(year) + "_denormalized.csv"
        with open(write_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(data_columns)
            writer.writerow(data)
        print(year, "- Denormalized, Complete")


if __name__ == '__main__':
    sort_annual()
