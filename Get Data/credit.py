import fetch
import csv
import os
import pandas as pd


def credit():
    fetch.get_credit()


if __name__ == "__main__":
    credit()
    fetch.flush_local()