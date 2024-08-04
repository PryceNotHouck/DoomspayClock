import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

housing_file = 'housing.csv'
inflation_file = 'inflation.csv'
loandefault_file = 'loandefault.csv'
cpi_file = 'cpi.csv'
cboe_file = 'cboe.csv'

housing_df = pd.read_csv(housing_file)
inflation_df = pd.read_csv(inflation_file)
loandefault_df = pd.read_csv(loandefault_file)
cpi_df = pd.read_csv(cpi_file)
cboe_df = pd.read_csv(cboe_file)

df = housing_df.merge(inflation_df, on='Year',  how='outer')\
                      .merge(loandefault_df, on='Year',  how='outer')\
                      .merge(cpi_df, on='Year',  how='outer')\
                      .merge(cboe_df, on='Year',  how='outer')


for column in df.columns[1:]:
    column_mean = df[column].mean()
    df.fillna({column: column_mean}, inplace=True)


columns_to_normalize = {
    'Average Median Price': 'positive',
    'Year-In Change': 'positive',
    'Average Business Loan Default Rate': 'negative',
    'Average All Loans Default Rate': 'negative',
    'Year-In Business Loan Default Change': 'negative',
    'Year-In All Loans Default Change': 'negative',
    'Average Interest Rate': 'negative',
    'Average Inflation Rate': 'negative',
    'Year-In Interest Rate Change': 'negative',
    'Year-In Inflation Rate Change': 'negative',
    'Gold Average': 'positive',
    'Oil Average': 'positive',
    'S&P 500 9-Day Average': 'positive',
    'VVIX Average': 'positive',
    'Apple Average': 'positive',
    'Amazon Average': 'positive',
    'EMVIX Average': 'positive',
    'Gold Delta': 'positive',
    'Oil Delta': 'positive',
    'S&P 500 9-Day Delta': 'positive',
    'VVIX Delta': 'positive',
    'Apple Delta': 'positive',
    'Amazon Delta': 'positive',
    'EMVIX Delta': 'positive',
    'Consumer Confidence': 'positive',
    'Consumer Confidence Delta': 'positive'
}

def normalize_columns(df, columns_to_normalize):
    scaler = MinMaxScaler()
    columns = list(columns_to_normalize.keys())
    df[columns] = scaler.fit_transform(df[columns])
    return df

normalized_df = normalize_columns(df, columns_to_normalize)

def calculate_economic_score(df, columns_to_normalize):
    scores = list(range(43))
    value = 0
    for index in scores:
        for column, impact in columns_to_normalize.items():
            if impact == 'positive':
                value = value + df[column][index]
            elif impact == 'negative':
                value = value + (1 - df[column][index])
        scores[index] = value
        value = 0

    return scores

economic_scores = calculate_economic_score(normalized_df, columns_to_normalize)

economic_scores_series = pd.Series(economic_scores)


scaler = MinMaxScaler(feature_range=(-1, 1))
normalized_economic_score = scaler.fit_transform(economic_scores_series.values.reshape(-1, 1)).flatten()
normalized_df['Economic Score'] = normalized_economic_score
normalized_df.to_csv('final_normalized_economic_scores.csv', index=False)
print(normalized_df[['Year', 'Economic Score']])


def test100000(df):
    data = np.random.rand(100, 1000)
    df = pd.DataFrame(data, columns=[f'col_{i}' for i in range(1000)])
    df['new_col'] = np.random.rand(100)


    return 0


test100000(normalized_df)