# Used Here: Python.org documentation on heapq

from sort_annual import sort_annual, flush_years
import os
import csv
import heapq


def priority_queue(data):
    # Priority Queue - Associate the index for each weight with its rank among all other weights, used to ensure that
    # all years' weights total up to +/- 1 if any values are missing.
    priority = []
    descending = sorted(data, reverse=True)
    for i in range(len(data)):
        for j in range(len(descending)):
            if data[i] == descending[j]:
                heapq.heappush(priority, (j+1, i))
    return priority


def adjust_midnight(data):
    # Supplements information about 2009 manually with values not available in the datasets used.
    data[2] = 84.42  # S&P 500 Average
    data[4] = 56.91  # Apple Volatility
    data[5] = 44.65  # Amazon Volatility
    data[6] = 26.23  # Emerging Market Volatility
    data[9] = -98.51  # S&P Delta
    data[10] = 76.56  # Apple Delta
    data[11] = 90.12  # Amazon Delta
    return data


def adjust_noon(data):
    # Supplements information about 1955 manually with values not available in the datasets used.
    data[0] = 15.0  # Gold Volatility
    data[1] = 10.0  # Oil Volatility
    data[2] = 12.35  # S&P 500 Average
    data[3] = 80.00  # VVIX Average
    data[4] = 15.20  # General Motors Volatility - Substituted for Apple, comparable impact
    data[5] = 16.10  # General Electric Volatility - Substituted for Amazon, comparable impact
    data[6] = 15.00  # Emerging Market Volatility
    data[7] = 2.10  # Gold Volatility Delta
    data[8] = 2.20  # Oil Volatility Delta
    data[9] = 0.18  # S&P Delta
    data[10] = 5.45  # VVIX Delta
    data[11] = 15.20  # GM Delta
    data[12] = 16.10  # GE Delta
    data[13] = 15.00  # Emerging Market Delta
    data[14] = 26.8  # Consumer Price Index
    data[15] = -0.3  # Consumer Price Delta
    data[16] = 1.82  # Average Consumer Loan Default Rate
    data[17] = 1.75  # Average All Loan Default Rate
    data[18] = 2.25  # Average Credit Delinquency
    data[19] = -0.45  # Consumer Loan Default Delta
    data[20] = 0.12  # All Loan Delta
    data[21] = 0.24  # Credit Delinquency Delta
    data[32] = 18400  # Median Housing Price
    data[33] = 0.00  # Median Delta
    data[34] = 2.29  # Average Interest Rate
    data[35] = -0.37  # Average Inflation Rate
    data[36] = 0.125  # Interest Rate Delta
    data[37] = 0.30  # Inflation Delta
    data[38] = 1.10  # Business Loan Default
    data[39] = 1.75  # Alt. Loan Default
    data[40] = -0.25  # Delta Business Loan Default
    data[41] = 0.12  # Alt. Loan Default Delta
    data[47] = 0  # Nonresidential
    data[48] = 0  # Equipment and Software
    data[49] = 0  # Residential
    data[50] = 0  # Equipment
    data[51] = 0  # Average Labor Force
    data[52] = 3.58  # Average Unemployment
    return data


def normalize_annual():
    sort_annual()
    weights = [0.005, 0.005, 0.02, 0.005, 0.005, 0.005, 0.005, 0, 0, 0.01, 0, 0, 0, 0, 0.025, 0.025, 0.01, 0.05, 0.01,
               0.01, 0.01, 0.01, 0, 0.05, 0, 0, 0, 0.01, 0.08, 0, 0.01, 0, 0.05, 0.1, 0.0375, 0.0375, 0.0375, 0.0375,
               0.025, 0.025, 0.025, 0.025, 0, 0.002, 0.002, 0.02, 0.002, 0.002, 0, 0.02, 0.002, 0, 0.20]
    priority_weights = priority_queue(weights)

    year_data_path = os.path.join(os.path.dirname(__file__), "Years")
    noon_data_path = os.path.join(os.path.dirname(__file__), "Years", "1955_denormalized.csv")
    midnight_data_path = os.path.join(os.path.dirname(__file__), "Years", "2009_denormalized.csv")

    noon = []
    midnight = []
    with open(noon_data_path, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        noon_str = reader.__next__()
        for val in noon_str:
            noon.append(float(val))
    with open(midnight_data_path, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        next(reader)
        midnight_str = reader.__next__()
        for val in midnight_str:
            midnight.append(float(val))
    noon = adjust_noon(noon)
    midnight = adjust_midnight(midnight)
    for i in range(len(weights)):
        noon[i] *= float(weights[i])
        midnight[i] *= float(weights[i])

    for file in os.listdir(year_data_path):
        file_path = os.path.join(os.path.dirname(__file__), "Years", file)
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            header = reader.__next__()
            next(reader)
            values_str = reader.__next__()
            next(reader)
            values = []
            local_weights = weights.copy()
            local_priority = priority_weights.copy()
            for val in values_str:
                values.append(float(val))
            for i in range(len(values)):
                if values[i] == 0 and i != len(values)-1:
                    dest = -1
                    for j in range(i):
                        test = heapq.heappop(local_priority)
                        if test[1] == i+1:
                            dest = test[1]
                    if dest == -1:
                        dest = heapq.heappop(local_priority)[1]
                    local_priority = priority_weights.copy()
                    local_weights[dest] += local_weights[i]
                    continue
                else:
                    values[i] *= local_weights[i]

            write_path = "Normalized Years/" + str(file[0:4]) + "_normalized.csv"
            with open(write_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(values)
            print(file[0:4], "- Normalized, Complete")


if __name__ == "__main__":
    normalize_annual()
    flush_years()
