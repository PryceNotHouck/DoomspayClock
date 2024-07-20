import fetch
from bea import gdp, trade
from cboe import cboe
from cpi import cpi
from credit import credit
from housing import housing
from inflation import inflation
from loandefault import loandefault
from unemployment import unemployment


def fetch_all():
    print("Unemployment Data:")
    unemployment()
    fetch.flush_local()
    print("-------------------------------")
    print("Loan Default Data:")
    loandefault()
    fetch.flush_local()
    print("-------------------------------")
    print("Inflation Data:")
    inflation()
    fetch.flush_local()
    print("-------------------------------")
    print("Housing Price Data:")
    housing()
    fetch.flush_local()
    print("-------------------------------")
    print("Credit Delinquency Data:")
    credit()
    fetch.flush_local()
    print("-------------------------------")
    print("Consumer Price Index Data:")
    cpi()
    fetch.flush_local()
    print("-------------------------------")
    print("Market Volatility Data:")
    cboe()
    fetch.flush_local()
    print("-------------------------------")
    print("GDP and GDP Sub-Variable Data:")
    gdp()
    print("-------------------------------")
    print("Trade and Foreign Investment Data:")
    trade()
    fetch.flush_local()
    print("-------------------------------")
    print("All collection complete.")


if __name__ == "__main__":
    fetch_all()
