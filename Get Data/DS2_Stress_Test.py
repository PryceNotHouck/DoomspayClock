# Used Here: PyPi.org page on timer 0.30

import pandas as pd
import heapq
import random
import logging
from timer import timer, get_timer


logging.basicConfig(level=logging.DEBUG)
timer.set_level(logging.DEBUG)
notif_timer = get_timer(logging.WARNING)

# Testing:

# def priority_queue(data):
#     priority = []
#     descending = sorted(data, reverse=True)
#     for i in range(len(data)):
#         for j in range(len(descending)):
#             if data[i] == descending[j]:
#                 heapq.heappush(priority, (j+1, i))
#     return priority


def make_test_set(n):
    global data
    data = []
    i = 0
    while i < n:
        i += 1
        data.append(i)
    random.shuffle(data)


def stress_test_pure():
    priority = []
    descending = sorted(data, reverse=True)
    with timer('stress_timer', unit='s') as t:
        for i in range(len(data)):
            for j in range(len(descending)):
                if data[i] == descending[j]:
                    heapq.heappush(priority, (j+1, i))
        print(f'Final Time: {t.elapse / 1000} s')


def stress_test_graph():
    graph_points = []
    priority = []
    descending = sorted(data, reverse=True)
    with timer('stress_timer', unit='s') as t:
        for i in range(len(data)):
            prev_time = float(t.elapse / 1000)
            for j in range(len(descending)):
                if data[i] == descending[j]:
                    heapq.heappush(priority, (j + 1, i))
                    graph_points.append([len(priority), float(t.elapse / 1000) - prev_time, float(t.elapse / 1000)])
    compiled = pd.DataFrame(graph_points, columns=['PQ Length', 'Time to Add', 'Total Time'])
    compiled.to_csv('DS2_graph_data.csv', index=False)
    print("DS2 Graph Data Complete")


if __name__ == '__main__':
    make_test_set(100000)
    stress_test_pure()
