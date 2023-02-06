'''
Author Li Shangkun
StuID 20307130215
CodingEnvironment MacBook Pro Python 3.9
'''

import baostock as bs
import pandas as pd
import mplfinance as mpf
import matplotlib as mpl
import matplotlib.pyplot as plt
import InputStockInfo

mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']
mpl.rcParams['axes.unicode_minus'] = False


def getStockData(stockcode, startdate, enddate, periodtype):  # 用于获取股票信息并返回一个含有股票信息的DataFrame数据结构
    bs.login()
    rs = bs.query_history_k_data_plus(stockcode, 'date, code, open, high, low, close',  # 获取股票信息
                                      start_date=startdate,
                                      end_date=enddate,
                                      frequency=periodtype)
    data_list = []
    while (rs.error_code == '0') & rs.next():  # 获取一条记录，并将多条记录整合在一起
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=['date', 'code', 'open', 'high', 'low', 'close'])  # 创建一个DataFrame数据结构
    df['open'] = df['open'].astype('float')  # 将获得的数据转换为浮点数类型
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['date'] = pd.to_datetime(df['date'])  # 将date列数据类型转换为时间类型
    df.set_index(['date'], inplace=True)  # 将日期列作为行索引
    bs.logout()
    return df


def candle_draw(data, fig1, ax1, title1):  # 画出K线图
    mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i')
    s = mpf.make_mpf_style(gridaxis='both', gridstyle='-.', y_on_right=False, marketcolors=mc)
    mpl.rcParams['lines.linewidth'] = 0.5
    font1 = {'family': 'Arial Unicode MS', 'weight': 'bold', 'size': 10, }
    ax1.set_title(title1, font1)
    kwargs = dict(type='candle', )
    mpf.plot(data, **kwargs, tight_layout=True, style=s, ax=ax1)
    fig1.canvas.draw_idle()


if __name__ == '__main__':
    rslt = InputStockInfo.main()  # 执行InputStockInfo.py中的main()
    if rslt[0] != '':
        if rslt[0].startswith('6'):  # 将股票代码补充完整
            stockcode = 'sh.'+rslt[0]
        else:
            stockcode = 'sz.'+rslt[0]
        startdate = rslt[1]   # 获得开始时间
        enddate = rslt[2]     # 获得截止时间
        periodtype = rslt[3]  # 获得K线种类
        if periodtype == 'day':
            StockData = getStockData(stockcode, startdate, enddate, 'd')
            title1 = '股票代码：' + stockcode[3:] + '(' + startdate + '~' + enddate + ')日K线图'
        elif periodtype == 'week':
            StockData = getStockData(stockcode, startdate, enddate, 'w')
            title1 = '股票代码：' + stockcode[3:] + '(' + startdate + '~' + enddate + ')周K线图'
        else:
            StockData = getStockData(stockcode, startdate, enddate, 'm')
            title1 = '股票代码：' + stockcode[3:] + '(' + startdate + '~' + enddate + ')月K线图'
    fig = plt.figure(figsize=(10, 7), dpi=100)
    left, width, bottom, top = 0.05, 0.9, 0.10, 0.80
    ax1 = fig.add_axes([left, bottom, width, top], gid='mygroup')
    candle_draw(StockData, fig, ax1, title1)
    fig.canvas.set_window_title('K线图')
    plt.show()
