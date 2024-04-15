# -*- coding: utf-8 -*-
"""
author: Napoleon
akshare的金融数据接口
"""

import akshare as ak
from czsc import Freq, RawBar
from typing import List


def format_kline(symbol, df, freq=Freq.D):
    """对K线进行格式化"""
    print(df.columns)
    bars = []
    for i, row in df.iterrows():
        # amount 单位：元
        bar = RawBar(symbol=symbol, id=i, freq=freq, dt=row['日期'] if '日期' in df.columns else row['时间'], open=round(row['开盘'], 2),
                     close=round(row['收盘'], 2), high=round(row['最高'], 2),
                     low=round(row['最低'], 2), vol=row['成交量'], amount=row['成交额'] if 'amount' in df.columns else 0)
        bars.append(bar)
    return bars


def get_raw_bars(symbol, freq, sdt, edt, fq='前复权', **kwargs) -> List[RawBar]:
    """
    获取 CZSC 库定义的标准 RawBar 对象列表

    :param symbol: 股票代码
    :param freq: K线周期，如 1分钟线为 Freq.F1
    :param sdt: 开始日期
    :param edt: 结束日期
    :param fq: 复权类型，默认为前复权
    :return: 标准 RawBar 对象列表
    """

    if fq == '前复权':
        adjust = 'qfq'
    elif fq == '后复权':
        adjust = 'hfq'
    else:
        assert fq == '不复权'
        adjust = ''
    if freq == Freq.D:
        period = 'daily'
    elif freq == Freq.W:
        period = 'weekly'
    elif freq == Freq.M:
        period = 'monthly'
    elif freq == Freq.F1:
        period = '1'
    elif freq == Freq.F5:
        period = '5'
    elif freq == Freq.F15:
        period = '15'
    elif freq == Freq.F30:
        period = '30'
    elif freq == Freq.F60:
        period = '60'
    else:
        raise ValueError("不支持的K线周期")

    if symbol.lower().startswith('sh') or symbol.lower().startswith('sz') or symbol.isdigit():
        if not symbol.isdigit():
            symbol = symbol[2:]
        # 获取数据, 使用数据为东财数据
        if freq == Freq.D or freq == Freq.W or freq == Freq.M:
            data = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=sdt, end_date=edt, adjust=adjust)
        elif freq == Freq.F1 or freq == Freq.F5 or freq == Freq.F15 or freq == Freq.F30 or freq == Freq.F60:
            data = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, start_date=sdt, end_date=edt, adjust=adjust)
        else:
            raise ValueError("不支持的K线周期")
    elif symbol.lower().startswith('hk'):
        symbol = symbol[2:].zfill(5)
        # 获取数据, 使用数据为港股数据
        if freq == Freq.D or freq == Freq.W or freq == Freq.M:
            data = ak.stock_hk_hist(symbol=symbol, period=period, start_date=sdt, end_date=edt, adjust=adjust)
        elif freq == Freq.F1 or freq == Freq.F5 or freq == Freq.F15 or freq == Freq.F30 or freq == Freq.F60:
            data = ak.stock_hk_hist_min_em(symbol=symbol, period=period, start_date=sdt, end_date=edt, adjust=adjust)
        else:
            raise ValueError("不支持的K线周期")
    else:
        raise ValueError("不支持的股票代码")

    return format_kline(symbol, data, freq)


if __name__ == '__main__':
    symbol = '000001'
    bars = get_raw_bars(symbol, Freq.D, '20200101', '20240412', fq='前复权')
    print(bars)

