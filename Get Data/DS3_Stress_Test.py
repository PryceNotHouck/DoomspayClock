import pandas as pd
import random
import logging
from timer import timer, get_timer


logging.basicConfig(level=logging.DEBUG)
timer.set_level(logging.DEBUG)
notif_timer = get_timer(logging.WARNING)

# Testing:

# data[years[point]].append([Weight, Value 1, Value 2, Variable ID]) - Adjacency List


def make_test_set(n):
    global data
    data = []
    i = 0
    while i < n:
        i += 1
        data.append(i)


def stress_test_graph():
    graph_points = []
    df = pd.DataFrame()
    for year in range(1929, 2024):
        df[year] = 0
    with timer('stress_timer', unit='s') as t:
        for i in range(len(data)):
            prev_time = float(t.elapse / 1000)
            df[random.randint(1929, 2023)] = data[i]
            graph_points.append([df.size, float(t.elapse / 1000) - prev_time, float(t.elapse / 1000)])
        print(f'Final Time: {t.elapse / 1000} s')
    compiled = pd.DataFrame(graph_points, columns=['DF Length', 'Time to Add', 'Total Time'])
    compiled.to_csv('DS3_graph_data.csv', index=False)
    print("DS3 Graph Data Complete")


if __name__ == '__main__':
    make_test_set(100000)
    stress_test_graph()
