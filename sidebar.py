import streamlit as st
import datetime

secondaryBackgroundColor = "#F0F2F6"


def choose_ticker_date(ticker, ticker_dict):
    with st.sidebar:
        st.header("Choose your parameters:")
        # ticker select box
        add_ticker = st.selectbox("Company name",
                                  ticker,
                                  format_func=ticker_dict.get)
        # start date
        start_date = st.date_input("Start date")
        # end date
        end_date = st.date_input("End date",
                                 max_value=datetime.date.today())
        # error output
        if start_date >= end_date:
            st.error("The start date must come before the end date")

        return add_ticker, start_date, end_date


# technical analysis
def add_volume():
    return st.checkbox(label="Add volume")


def add_sma():
    """
    Takes SMA-Parameters
    :return:
        - Flag
        - Period
    """
    sma_expander = st.expander("Simple Moving Average (SMA)")
    sma_flag = sma_expander.checkbox(label="Add SMA")
    sma_periods = sma_expander.slider(
        label="SMA Periods",
        min_value=1,
        max_value=50,
        value=20,
        step=1
    )
    return sma_flag, sma_periods


def add_ema():
    """
    Takes EMA-Parameters
    :return:
        - Flag
        - Period
    """
    ema_expander = st.expander("Exponential Moving Average (EMA)")
    ema_flag = ema_expander.checkbox(label="Add EMA")
    ema_periods = ema_expander.slider(label="EMA Periods",
                                      min_value=1,
                                      max_value=50,
                                      value=20,
                                      step=1)
    return ema_flag, ema_periods


def add_macd():
    """
    Takes MACD-parameters
    :return:
        - Flag
        - Period
        - Fast Period
        - Slow Period
        - Signal
    """
    macd_expander = st.expander(label="Moving Average Convergence Divergence (MACD)")
    macd_flag = macd_expander.checkbox("Add MACD")
    macd_fast = macd_expander.slider(label="Fast Period",
                                     min_value=5,
                                     max_value=25,
                                     value=12,
                                     step=1)
    macd_slow = macd_expander.slider(label="Slow Period",
                                     min_value=20,
                                     max_value=52,
                                     value=26,
                                     step=1)
    macd_signal = macd_expander.slider(label="Signal",
                                       min_value=1,
                                       max_value=20,
                                       value=9,
                                       step=1)
    if not macd_signal < macd_fast < macd_slow:
        macd_expander.error("This is not right. Please refer to the help section.")

    return macd_flag, macd_fast, macd_slow, macd_signal


def add_bb():
    """
    Takes Bollinger Bands-Parameteres
    :return:
        - Flag
        - Periods
        - standard deviation
    """
    bb_expander = st.expander("Bollinger Bands")
    bb_flag = bb_expander.checkbox(label="Add Bollinger Bands")
    bb_periods = bb_expander.slider(label="Periods",
                                          min_value=1,
                                          max_value=50,
                                          value=20,
                                          step=1)
    bb_std = bb_expander.slider(label="Standard deviation",
                                      min_value=1,
                                      max_value=4,
                                      value=2,
                                      step=1)
    return bb_flag, bb_periods, bb_std


def add_rsi():
    """
    Takes RSI-Parameters
    Return:
        - RSI Flag
        - RSI Period
        - RSI lower
        - RSI upper
    """
    rsi_expander = st.expander("Relative Strength Index (RSI)")
    rsi_flag = rsi_expander.checkbox("Add RSI")
    rsi_period = rsi_expander.slider(label="RSI Periods",
                                     min_value=1,
                                     max_value=50,
                                     value=20,
                                     step=1)
    rsi_lower = rsi_expander.slider(label="RSI Lower",
                                    min_value=10,
                                    max_value=50,
                                    value=30,
                                    step=1)
    rsi_upper = rsi_expander.slider(label="RSI Upper",
                                    min_value=50,
                                    max_value=90,
                                    value=70,
                                    step=1)

    return rsi_flag, rsi_period, rsi_lower, rsi_upper