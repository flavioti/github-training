import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

pd.options.display.float_format = "{:.2f}".format

st.set_page_config(layout="wide")

st.title("Deriv bot")


def fb_reload():
    st.cache_data.clear()


st.button("Clear cache", on_click=fb_reload)


@st.cache_data(ttl=10, show_spinner=bool)
def get_data():
    print("reloading...")
    df = pd.read_csv("log.csv", delimiter=";")
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["saldo"] = df["saldo"].str.replace(",", ".").astype(float)

    novo_saldo = df.tail(1)["saldo"].max()
    velho_saldo = st.session_state.get("saldo", novo_saldo)

    if novo_saldo > velho_saldo:
        st.balloons()
    elif novo_saldo < velho_saldo:
        st.snow()

    st.session_state["saldo"] = novo_saldo
    return df


df_full = get_data()

df = df_full.copy()

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

won_count: int = len(df[df["position"] == "Won"])
lost_count: int = len(df[df["position"] == "Lost"])

try:
    taxa_ganho = lost_count / won_count * 100
except Exception:
    taxa_ganho = 0

col1.metric(label="Won", value=won_count, help="Inteiro")
col2.metric(label="Lost", value=lost_count, help="Inteiro")
col3.metric(label="Lost rate (good <8%)", value=f"{taxa_ganho:10.1f}" + " %", help="Percentual")
col4.metric(label="Saldo", value=df.iloc[-1, 38])
col5.metric(label="Saldo minimo", value=df["saldo"].min())
col6.metric(label="Saldo máximo", value=df["saldo"].max())


exp1 = st.expander("Percentuais", expanded=False)
per0, per1, per2, per3, per4, per5, per6, per7, per8, per9 = exp1.columns(10, gap="small")

df_metric = df.copy().tail(100)

per0.metric(label="0", value=df_metric.iloc[-1, 28])
per1.metric(label="1", value=df_metric.iloc[-1, 29])
per2.metric(label="2", value=df_metric.iloc[-1, 30])
per3.metric(label="3", value=df_metric.iloc[-1, 31])
per4.metric(label="4", value=df_metric.iloc[-1, 32])
per5.metric(label="5", value=df_metric.iloc[-1, 33])
per6.metric(label="6", value=df_metric.iloc[-1, 34])
per7.metric(label="7", value=df_metric.iloc[-1, 35])
per8.metric(label="8", value=df_metric.iloc[-1, 36])
per9.metric(label="9", value=df_metric.iloc[-1, 37])

del df_metric

df = df[["data_hora", "position", "saldo"]][(df["position"] == "Won") | (df["position"] == "Lost")]

cold1, cold2 = st.columns([2, 6], gap="small")

cold1.dataframe(df.sort_values(by="data_hora", ascending=False))

df["data_hora"] = df["data_hora"].astype("string")
df["data_hora"] = df["data_hora"].str[8:19]

valor = cold2.slider(
    label="Quantidade de apostas a serem exibidas",
    min_value=10,
    max_value=1000,
    value=100,
    step=1,
)

fig = px.histogram(
    df.tail(valor),
    x="data_hora",
    y="saldo",
    cumulative=False,
    hover_data=df.columns,
    hover_name=df.tail(valor)["position"],
    title="Saldo",
)


cold2.plotly_chart(fig, use_container_width=True)

df_full["digito_atual"] = df_full["digito_atual"].astype(int)

hist_data = [df_full["digito_atual"], df_full["menor_atual"]]
group_labels = ["digito", "menor"]  # name of the dataset

fig = ff.create_distplot(hist_data=hist_data, group_labels=group_labels, curve_type="kde")

st.plotly_chart(fig)

# st.dataframe(df_full)
