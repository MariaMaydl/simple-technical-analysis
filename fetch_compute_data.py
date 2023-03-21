import yfinance as yf
import pandas as pd
import datetime
import streamlit as st

SP500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

@st.cache_data
def get_sp500_members():
    """
    Access Sp500 companies via link and saves the ticker and company names
    :return:
    tickers = List of tickers
    dict_names = Dictionary of tickers and company names
    """
    df = pd.read_html(SP500)[0]
    tickers = df["Symbol"].to_list()
    dict_company_names = dict(zip(df["Symbol"], df["Security"]))
    return tickers, dict_company_names


# load data
@st.cache_data
def load_data(ticker, start, end):
    """
    Loads data from yahoo finance
    :param ticker: Takes as input the Ticker
    :param start: Start date
    :param end: End date
    :return: Returns downloaded data from yahoo finance
    """
    return yf.download(ticker, start, end)


# save to csv
@st.cache_data
def save_to_csv(df):
    """
    :param df: Takes pandas dataframe
    :return: returns encoded csv
    """
    return df.to_csv().encode("utf-8")


def preview_save_date(df):
    df_expander = st.expander("Preview of the data")
    df_columns = df.columns.to_list()
    df_pick_columns = df_expander.multiselect("Columns",
                                              df_columns,
                                              default=df_columns)
    df_expander.dataframe(df[df_columns])

    csv_file = save_to_csv(df[df_columns])
    df_expander.download_button(
        label="Download as CSV file",
        data=csv_file,
        file_name=f"Stock_prices.csv",
        mime="text/csv"
    )

