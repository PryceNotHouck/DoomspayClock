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
        data.append([random.randint(1929, 2023), random.randint(1, 1000), random.randint(1, 1000),
                     random.randint(1, 1000)])


def stress_test_pure():
    adj_list = {}
    with timer('stress_timer', unit='s') as t:
        for i in range(len(data)):
            year = random.randint(1929, 2023)
            try:
                adj_list[year] += [data[i][0], data[i][1], data[i][2], data[i][3]]
            except KeyError:
                adj_list[year] = []
                adj_list[year] += [data[i][0], data[i][1], data[i][2], data[i][3]]
        print(f'Final Time: {t.elapse / 1000} s')


def stress_test_graph():
    graph_points = []
    items_added = 0
    adj_list = {}
    with timer('stress_timer', unit='s') as t:
        for i in range(len(data)):
            prev_time = float(t.elapse / 1000)
            year = random.randint(1929, 2023)
            try:
                adj_list[year] += [data[i][0], data[i][1], data[i][2], data[i][3]]
            except KeyError:
                adj_list[year] = []
                adj_list[year] += [data[i][0], data[i][1], data[i][2], data[i][3]]
            items_added += 4
            graph_points.append([items_added, float(t.elapse / 1000) - prev_time, float(t.elapse / 1000)])
        print(f'Final Time: {t.elapse / 1000} s')
    compiled = pd.DataFrame(graph_points, columns=['AL Length', 'Time to Add', 'Total Time'])
    compiled.to_csv('DS1_graph_data.csv', index=False)
    print("DS1 Graph Data Complete")


if __name__ == '__main__':
    make_test_set(100000)
    stress_test_pure()
