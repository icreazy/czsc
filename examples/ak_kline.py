"""
ak kline
"""

from czsc.connectors.ak_connector import get_raw_bars
from czsc.analyze import CZSC
from czsc.enum import Freq
import streamlit as st
import streamlit_echarts
from datetime import date, timedelta

if __name__ == '__main__':
    # 设置页面自适应
    st.set_page_config(layout="wide")
    with st.sidebar:
        symbol = st.text_input('请输入股票代码:', 'HK02333')
        start_date = st.date_input('请输入开始日期:', value=date.today() + timedelta(days=-30))
        end_date = st.date_input('请输入结束日期:', value=date.today())
        fq = st.selectbox('复权方式:', ['前复权', '后复权', '不复权'])
        query = st.button('查询')

    if query:
        streamlit_echarts.st_pyecharts(
            CZSC(
                get_raw_bars(symbol, Freq.W, min(start_date, end_date + timedelta(days=-365)), end_date, fq=fq)
            ).to_echarts(), height="600px", key="weekly")

        streamlit_echarts.st_pyecharts(
            CZSC(
                get_raw_bars(symbol, Freq.D, min(start_date, end_date + timedelta(days=-150)), end_date, fq=fq)
            ).to_echarts(), height="600px", key="daily")

        streamlit_echarts.st_pyecharts(
            CZSC(
                get_raw_bars(symbol, Freq.F30, start_date, end_date, fq=fq)
            ).to_echarts(), height="600px", key="30m")

        streamlit_echarts.st_pyecharts(
            CZSC(
                get_raw_bars(symbol, Freq.F5, start_date, end_date, fq=fq)
            ).to_echarts(), height="600px", key="5m")
