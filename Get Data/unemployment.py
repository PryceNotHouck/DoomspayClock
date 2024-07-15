import fetch
import pandas as pd
import os


def process_file(file, data):
    print("Reading:", file)
    file_path = os.path.join(os.path.dirname(__file__), "Local", file)
    df = pd.read_csv(file_path, skiprows=6)

    year = int(df.iloc[0, 4])
    df.iloc[:, 6] = pd.to_numeric(df.iloc[:, 6], errors='coerce')
    df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')

    avg_labor_force = int(df.iloc[:, 6].mean(skipna=True))
    avg_unemployment = df.iloc[:, 9].mean(skipna=True)

    # print(year, "'s, average labor:", avg_labor_force)
    # print(year, "'s, average unemployment:", avg_unemployment)
    data.append([year, avg_labor_force, avg_unemployment])
    return data


def unemployment():
    print("Fetching Data")
    fetch.get_unemployment()
    data = []
    local_path = os.path.join(os.path.dirname(__file__), "Local")

    for file in os.listdir(local_path):
        data = process_file(file, data)

    fetch.flush_local()

    compiled = pd.DataFrame(data, columns=['Year', 'Average Labor Force', 'Average Unemployment'])
    compiled.to_csv('unemployment.csv', index=False)
    print("Unemployment Complete")


if __name__ == "__main__":
    unemployment()
    fetch.flush_local()
