'''
Author Li Shangkun
StuID 20307130215
CodingEnvironment MacBook Pro Python 3.9
'''
import tkinter as tk
from tkinter import ttk
stockInfo = ['', '', '', '']


def main():
    root = tk.Tk()
    root.title('输入股票代码和起止时间')  # 界面的标题
    root.geometry('470x200')  # 界面大小
    label1 = tk.Label(root, text='股票代码(如:600215):')  # 设置输入框
    label1.place(x=20, y=5, width=200, height=25)
    editbox1 = tk.Entry(root)
    editbox1.place(x=225, y=5, width=200, height=25)
    label2 = tk.Label(root, text='开始时间(如2020-03-01):')
    label2.place(x=20, y=45, width=200, height=25)
    editbox2 = tk.Entry(root)
    editbox2.place(x=225, y=45, width=200, height=25)
    label3 = tk.Label(root, text='截止时间(如2021-03-01):')
    label3.place(x=20, y=85, width=200, height=25)
    editbox3 = tk.Entry(root)
    editbox3.place(x=225, y=85, width=200, height=25)
    label4 = tk.Label(root, text='K线类型:')
    label4.place(x=20, y=125, width=200, height=25)
    comvalue = tk.StringVar()  # 可以随时根据用户的选择更新窗体中的值
    comboxlist = ttk.Combobox(root, textvariable=comvalue)  # 创建一组合框，可选择K线种类
    comboxlist['values'] = ('日K线', '周K线', '月K线')  # 设置组合框中的值
    comboxlist.place(x=225, y=125, width=200, height=25)

    def myConfirm():  # GUI界面中点击"确定"后执行，获取将输入框中的数据填充进stockInfo中
        global stockInfo
        var1 = editbox1.get()
        var2 = editbox2.get()
        var3 = editbox3.get()
        var4 = comboxlist.get()
        if var1 != '' and var2 != '' and var3 != '' and var4 != '':
            if var4 == '日K线':
                var4 = 'day'
            elif var4 == '周K线':
                var4 = 'week'
            elif var4 == '月K线':
                var4 = 'month'
            stockInfo = [var1, var2, var3, var4]
            root.quit()

    def myCancel():  # GUI界面中点击"取消"后执行，直接退出GUI界面
        global stockInfo
        stockInfo = ['', '', '']
        root.quit()

    button1 = tk.Button(root, text='确定', command=myConfirm)  # 设计"确定"按钮
    button1.place(x=95, y=165, width=40, height=25)
    button2 = tk.Button(root, text='取消', command=myCancel)  # 设计"取消"按钮
    button2.place(x=330, y=165, width=40, height=25)
    root.focus_force()
    editbox1.focus_force()
    root.mainloop()
    root.destroy()
    return stockInfo
