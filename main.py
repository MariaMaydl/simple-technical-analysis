# Import and go in offline mode for cufflinks
import cufflinks as cf
import openai
from sidebar import *
from fetch_compute_data import *
from plotly.offline import iplot

cf.go_offline()

openai.api_key = st.secrets["api_key"]
MODEL_ENGINE = "text-davinci-003"


@st.cache_resource
def gpt_help(question):
    """
    Gets the user input, pass it to the algorithm and displays the answer
    :return:  response
    """
    # use OPENAI to generate the response
    completion = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=question,
        max_tokens=1024,
        n=1,
        temperature=0.5,
        stop=None
    )
    response = completion.choices[0].text
    return st.write(response)


def visualize_user_manual():
    st.title("Simple Technical Analysis for SP500")
    # User manual
    st.header("_User Manual:_")
    st.write("""
    * you can choose any company from the SP500 index
    * in the sidebar you determine the start and end date for the analysis
    * you can download the selected data as CSV file in the preview-section
    * you can add several technical Indicators: 
        * SMA (Simple Moving Average)
        * EMA (Exponential Moving Average)
        * MACD (Moving Average Convergence Divergence)
        * Bollinger Bands
        * RSI (Relative Strength Index)
    * Need help? Scroll down to the help section.
    """)


if __name__=='__main__':
    # visualize user manual
    visualize_user_manual()
    # get tickers and dictionary of sp500
    sp500_ticker, ticker_company_dict = get_sp500_members()
    # get ticker, start and end date
    tickers, start_date, end_date = choose_ticker_date(sp500_ticker, ticker_company_dict)
    # fetch data from yfinance
    df = load_data(tickers, start_date, end_date)
    # first function: preview and save data
    preview_save_date(df)

    # technical analysis
    with st.sidebar:
        volume_flag = add_volume()
        sma_flag, sma_period = add_sma()
        ema_flag, ema_period = add_ema()
        macd_flag, macd_fast, macd_slow, macd_signal = add_macd()
        bb_flag, bb_period, bb_std = add_bb()
        rsi_flag, rsi_period, rsi_lower, rsi_upper = add_rsi()

    # plot technical analysis
    qf = cf.QuantFig(df, title=f"{ticker_company_dict[tickers]}")
    if volume_flag:
        qf.add_volume()
    if sma_flag:
        qf.add_sma(periods=sma_period)
    if ema_flag:
        qf.add_ema(periods=ema_period)
    if macd_flag:
        qf.add_macd(macd_fast, macd_slow, macd_signal)
    if bb_flag:
        qf.add_bollinger_bands(periods=bb_period, boll_std=bb_std)
    if rsi_flag:
        qf.add_rsi(periods=rsi_period,
                   rsi_upper=rsi_upper,
                   rsi_lower=rsi_lower,
                   showbands=True)
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)

    # help section
    st.subheader("Need help?")
    user_question = st.text_input("Ask your question about technical financial analysis")
    gpt_help(user_question)

