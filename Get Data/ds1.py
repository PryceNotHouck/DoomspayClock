import pandas as pd

df = pd.read_csv('DS1_graph_data.csv')

df.to_excel('DS1.xlsx', index=False)