'''
Author Li Shangkun
Stu_ID 20307130215
Coding Environment macOS 11.2.3 Python 3.9
'''

import baostock as bs  # 引入程序所需要的库
import pandas as pd
import mplfinance as mpf
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
mpl.rcParams['axes.unicode_minus'] = False  # 设置负号显示
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置中文显示


def getStockData(stockcode, startdate, enddate, periodtype):  # 用于获取股票信息并返回一个含有股票信息的DataFrame数据结构
    bs.login()  # 登陆系统
    rs = bs.query_history_k_data_plus(stockcode, "date,code,open,high,low,close",
                                      start_date=startdate,
                                      end_date=enddate,
                                      frequency=periodtype)
    data_list = []
    while (rs.error_code == '0') & rs.next():  # 获取一条记录，并将记录合并在一起
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=["date", "code", "open", "high", "low", "close"])  # 创建一个DataFrame数据结构
    df['open'] = df['open'].astype('float')   # 将获得的数据转换为浮点数类型
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['date'] = pd.to_datetime(df['date'])  # 将date列数据类型转换为时间类型
    df.set_index(['date'], inplace=True)  # 将日期列作为行索引
    bs.logout()
    return df


def candle_draw(data, fig1, ax1, title1):
    mc = mpf.make_marketcolors(    # 设置marketcolors
        up='red',                  # 设置收盘价大于等于开盘价时K线线柱的颜色
        down='green',              # 设置收盘价小于开盘价时K线线柱的颜色
        edge='i',                  # 设置K线线柱边缘的颜色，i表示继承自up和down的颜色，下同
        wick='i')                  # 设置上下影线的颜色
    s = mpf.make_mpf_style(        # 设置图形风格
        gridaxis='both',           # 设置网格线位置
        gridstyle='-.',            # 设置网格线线型
        y_on_right=False,          # 设置y轴位置是否在右
        marketcolors=mc)
    mpl.rcParams['lines.linewidth'] = 0.5
    font1 = {'family': 'Arial Unicode MS',  # 设置字体样式
             'weight': 'bold',
             'size': 10, }
    ax1.set_title(title1, font1)  # 设置标题
    kwargs = dict(type='candle',)  # 设置基本参数，其中type选择K线图
    mpf.plot(data, **kwargs, tight_layout=True, style=s, ax=ax1)
    fig1.canvas.draw_idle()


if __name__ == '__main__':
    stockcode = input('请输入学号的最后三位：')
    index = stockcode
    allStockLstFile = 'stock_basic.csv'
    with open(allStockLstFile, 'r', encoding='gbk') as fh:  # 从所有股票代码中找到包含输入3位数字的股票代码
        while True:
            line = fh.readline()
            if not line:
                break
            tmpinfo = line.strip('\n').split(',')
            if tmpinfo[4] == '1' and tmpinfo[5] == '1':  # 去掉股票代码中的'sh.'或'sz.'，并查看是否包含输入的3位数字，防止用户输入字母
                if stockcode in tmpinfo[0][3:]:
                    stockcode = tmpinfo[0]
                    break

    if len(stockcode) != 9:  # 如果没有找到相应的股票代码
        print('未找到最后三位为{}的股票'.format(index))
        sys.exit()

    startdate = "2021-02-01"   # 设置起止时间
    enddate = "2021-02-28"
    stockData = getStockData(stockcode, startdate, enddate, 'd')  # 获取股票信息
    fig = plt.figure(figsize=(12, 7), dpi=100)  # 绘制K线
    left, width, bottom, top = 0.05, 0.9, 0.10, 0.80
    ax1 = fig.add_axes([left, bottom, width, top], gid='mygroup')
    title = "股票代码"+stockcode[3:]+"("+startdate+"~"+enddate+")日K线图"  # 设置图表标题
    candle_draw(stockData, fig, ax1, title)
    aa = fig.canvas.manager.toolbar
    fig.canvas.set_window_title('K线图')
    plt.show()
