import altair as alt
import pandas as pd
import streamlit as st

pd.options.display.float_format = "{:.2f}".format


st.set_page_config(layout="wide")

st.title("Deriv bot")

df = pd.read_csv("log.csv", delimiter=";")

df["data_hora"] = pd.to_datetime(df["data_hora"])
df["saldo"] = df["saldo"].str.replace(",", ".").astype(float)


col1, col2, col3, col4 = st.columns(4)

won_count: int = len(df[df["position"] == "Won"])
lost_count: int = len(df[df["position"] == "Lost"])

try:
    taxa_ganho = lost_count / won_count * 100
except Exception:
    taxa_ganho = 0

col1.metric(label="Won", value=won_count, help="Inteiro")
col2.metric(label="Lost", value=lost_count, help="Inteiro")
col3.metric(label="Lost rate (good <=12%)", value=f"{taxa_ganho:10.1f}" + " %", help="Percentual")
col4.metric(label="Saldo", value=df.iloc[-1, 38])

per0, per1, per2, per3, per4, per5, per6, per7, per8, per9 = st.columns(10)

per0.metric(label="0", value=df.iloc[-1, 28])
per1.metric(label="1", value=df.iloc[-1, 29])
per2.metric(label="2", value=df.iloc[-1, 30])
per3.metric(label="3", value=df.iloc[-1, 31])
per4.metric(label="4", value=df.iloc[-1, 32])
per5.metric(label="5", value=df.iloc[-1, 33])
per6.metric(label="6", value=df.iloc[-1, 34])
per7.metric(label="7", value=df.iloc[-1, 35])
per8.metric(label="8", value=df.iloc[-1, 36])
per9.metric(label="9", value=df.iloc[-1, 37])


coll1, coll2 = st.columns(2)

coll1.dataframe(df[df["apostar"] == True].sort_values(by="data_hora", ascending=False))


c = (
    alt.Chart(df[df["apostar"] == True].tail(100)[["apostar", "data_hora", "saldo"]])
    .mark_line()
    .encode(
        x="data_hora",
        y="saldo",
    )
)

coll2.altair_chart(c, use_container_width=True)
