from unemployment import unemployment_points
from loandefault import loandefault_points
from inflation import inflation_points
from housing import housing_points
from cboe import cboe_points
from cpi import cpi_points


def datapoints():
    unemployment = unemployment_points()
    loan = loandefault_points()
    inflation = inflation_points()
    housing = housing_points()
    cboe = cboe_points()
    cpi = cpi_points()
    total = unemployment + loan + inflation + housing + cboe + cpi

    print()
    print()
    print("Unemployment Data Points:", f'{unemployment:,}')
    print("Loan Default Data Points:", f'{loan:,}')
    print("Inflation Data Points:", f'{inflation:,}')
    print("Housing Data Points:", f'{housing:,}')
    print("CBOE Data Points:", f'{cboe:,}')
    print("CPI Data Points:", f'{cpi:,}')
    print("---------------------------------")
    print("Total:", f'{total:,}')


if __name__ == "__main__":
    datapoints()
