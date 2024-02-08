import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st


st.title('U.S. Stock Price List App')


st.sidebar.write("""
                 
# MAGNIFICENT 7　株価
以下のオプションから表示日数を変更できます。   
                               
""")

st.sidebar.write("""
## 表示日数選択   
                               
""")
days= st.sidebar.slider('日数',0,365,30)


st.sidebar.write("""
## 株価範囲指定   
                               
""")

ymin,ymax=st.sidebar.slider(
    '範囲を指定してください。',
    0.0,3500.0,(0.0,3500.0))

st.write(f"""
### 過去 **{days}日間** の株価 
""")

@st.cache_data
def get_date(days,tickers):
    df=pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist=tkr.history(period=f'{days}d')
        hist.index=hist.index.strftime('%d,%B,%Y')
        hist=hist[['Close']]
        hist.columns=[company]
        hist=hist.T
        hist.index.name='Name'
        df=pd.concat([df,hist])
    return df
try:
    tickers={
        'Apple':'AAPL',
        'Meta':'META',
        'Google':'GOOGL',
        'Microsoft':'MSFT',
        'Amazon':'AMZN',
        'Ndivia':'NVDA',
        'Tesla':'TSLA'
    }

    df=get_date(days,tickers)
    companies=st.multiselect(
        '会社を選択してください。',
        list(df.index),
        ['Google','Apple','Meta','Amazon']

    )

    if not companies:
        st.error('少なくとも一社は選択してください。')
    else:
        data=df.loc[companies]
        st.write('### 株価(USD)' ,data.sort_index())
        data=data.T.reset_index()
        data=pd.melt(data,id_vars=['Date']).rename(
            columns={'value':'Stock Prices(USD)'})

        chart=(
            alt.Chart(data)
            .mark_line(opacity=0.8,clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q",stack=None,scale=alt.Scale(domain=[ymin,ymax])),
                color="Name:N"
        
            )

        )

        st.altair_chart(chart,use_container_width=True)
except:
    st.error('おっと！何か問題が発生したようです。')
