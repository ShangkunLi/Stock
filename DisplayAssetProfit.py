'''
Author Li Shangkun
StuID 20307130215
CodingEnvironment macOS 11.2.3 Python 3.9
'''

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import baostock as bs
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置字体样式
mpl.rcParams['axes.unicode_minus'] = False  # 设置负号显示
mpl.rcParams['lines.linewidth'] = 1.2  # 设置曲线宽度


def getStockData(stockcode, startdate, enddate, periodtype):
    bs.login()  # 登陆系统
    rs = bs.query_history_k_data_plus(stockcode, 'date, code, open, high, low, close, volume, amount, adjustflag, turn, pctChg',
                                      start_date=startdate,
                                      end_date=enddate,
                                      frequency=periodtype,
                                      adjustflag='3')
    # 获取对应股票的信息，volume为成交量，amount为成交额，adjustflag为复权状态，turn为换手率，pctChg为涨跌幅
    data_list = []
    while (rs.error_code == '0') & rs.next():  # 获取一条记录，并将多条记录整合在一起
        data_list.append(rs.get_row_data())
    capital = 0                                # 计算资产和收益率
    for i in range(len(data_list)):
        data = data_list[i]
        close = float(data[5])
        capital = capital + close*100
        tvalue = (close*(i+1)*100)
        profit = (tvalue/capital-1)*100
        data.append(capital)
        data.append(tvalue)
        data.append(profit)
    df = pd.DataFrame(data_list, columns=['date', 'code', 'open', 'high', 'low', 'close',
                                          'volume', 'amount', 'adjustflag', 'turn', 'pctChg',
                                          'capital', 'mktValue', 'profitRatio'])
    # 创建一个DataFrame数据结构
    df['open'] = df['open'].astype('float')  # 将获得的数据转换为浮点数类型
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['volume'] = df['volume'].astype('float')
    df['date'] = pd.to_datetime(df['date'])  # 将date列数据类型转换为时间类型
    df.set_index(['date'], inplace=True)  # 将日期列作为行索引
    bs.logout()
    return df


def main(stockcode, asset_info, s_dateStr, e_dateStr):
    linewidth_bak = mpl.rcParams['lines.linewidth']
    root = tk.Tk()
    root.geometry('1200x450+200+200')  # 设置窗口的大小与位置
    titlestr = stockcode + '资产与收益率曲线（' + s_dateStr + '~' + e_dateStr + ')'  # 设置曲线标题
    root.title(titlestr)
    fig = plt.figure(figsize=(8, 4), dpi=100)  # 设置图表的大小与分辨率
    left, width = 0.05, 0.90
    ax1 = fig.add_axes([left, 0.26, width, 0.70], gid='mygroup')
    ax2 = fig.add_axes([left, 0.05, width, 0.25], sharex=ax1, gid='mygroup')  # 共享ax1轴
    ax1.yaxis.grid(True, which='major')
    ax2.yaxis.grid(True, which='major')
    add_plot = [mpf.make_addplot(asset_info['mktValue'], color='red', width=0.5, ax=ax1),
                mpf.make_addplot(asset_info['profitRatio'], color='blue', width=1.2, ax=ax2)]
    mpf.plot(asset_info, ax=ax1, addplot=add_plot)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def QuitButton():  # 设计一个GUI交互界面，界面中点击"Quit"退出程序
        root.quit()
    button = tk.Button(root, text='Quit', command=QuitButton)
    button.pack(side=tk.BOTTOM)
    root.focus_force()
    root.mainloop()
    root.destroy()
    mpl.rcParams['lines.linewidth'] = linewidth_bak


if __name__ == '__main__':
    stockcode = 'sh.600215'  # 设置要处理的股票代码
    s_dateStr = '2021-02-01'  # 设置投资的起止时间
    e_dateStr = '2021-02-10'
    stockData_day = getStockData(stockcode, s_dateStr, e_dateStr, 'd')  # 获取对应股票的数据
    totalCapital = stockData_day['capital'][-1]  # 计算总本金投入
    totalmktValue = stockData_day['mktValue'][-1]  # 计算总资产
    totalProfit = totalmktValue-totalCapital  # 计算总收益
    profitRatio = stockData_day['profitRatio'][-1]  # 计算收益率
    maxloseRatio = stockData_day['profitRatio'].min()  # 计算最大回撤率
    if maxloseRatio > 0:
        maxloseRatio = 0
    print('总本金投入：{}'.format(totalCapital))  # 打印出数据
    print('期末总资产：{}'.format(totalmktValue))
    print('期末总收益：{}'.format(totalProfit))
    print('收益率：{:.5}%'.format(profitRatio))
    print('最大回撤率：{:.5}%'.format(maxloseRatio))
    main(stockcode, stockData_day, s_dateStr, e_dateStr)  # 画出资产与收益率曲线

