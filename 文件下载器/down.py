import requests
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import time
import zipfile
import random
from fake_useragent import UserAgent
from configparser import ConfigParser
import threading
import win32api
import win32con


def get_copy():
    win32api.keybd_event(17, 0, 0, 0)  #ctrl键位码是17
    win32api.keybd_event(67, 0, 0, 0)   #c键位码是67
    win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)    #释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
 
def get_paste():
    win32api.keybd_event(17, 0, 0, 0)  #ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)   #v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)    #释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


# 选择文件安放的位置
def get_wen():
    # 使用文件对话框选择文件
    # filedialog.askopenfilenames可以返回多个文件名
    data_1 = tkinter.filedialog.askdirectory(title="选择文件路径")
    data = data_1.replace('/' , r'\\')
    # print(type(data),data)
    # exit()
    entry_2.delete(0, END)
    entry_2.insert(0, data)

# 主函数
def get_zhu():
    ua = UserAgent()
    url = str(entry_1.get())
    header = {'User-Agent': ua.random}
    # print(header , url)
    # exit()
    """设置代理IP，如果只是本地测试，可以用你自己电脑的ip，不用设置代理IP"""
    # target = ConfigParser()
    # target.read('代理IP.ini', encoding='utf-8')
    # pwd = target.get('IP', 'ip')
    # ip_list = eval(pwd)
    # ip = random.choices(ip_list)[0]
    """设置IP，百度搜索'IP'显示的IP地址"""
    ip = {'ip':'114.245.189.116'}
    # 下载的文件名
    filename = url.rpartition('/')[-1]
    response = requests.get(url, headers=header , proxies= ip , stream=True)
    if response.status_code == 200:
        # 文件的总长度
        zhong_wen = int(response.headers['content-length'])
        # 下载文件的长度
        data_wen = 0
        name = entry_2.get() + r"\\" + filename
        with open(name, 'ab') as fp:
            for chunk in response.iter_content(chunk_size=512):
                # 下载中的文件
                data_wen += len(chunk)
                # 将下载文件占下载总文件以百分比的形式显示
                now_pross = (data_wen / zhong_wen) * 420
                # print(now_pross)
                # 用进度条来显示下载进度
                fill_line = canvas.create_rectangle(1, 1.5, 0, 23, width=0, fill="green")
                canvas.coords(fill_line, (0, 0, now_pross, 60))
                window.update()
 
                fp.write(chunk)
            lable1_4 = Label(window, text="100%", font=('微软雅黑', 15), fg='black', bg="green")
            lable1_4.place(x=300, y=160)
            time.sleep(1)
            tkinter.messagebox.showinfo(title='操作结果', message='文件下载完成')
    else:
        print("1")
 
def thread_it(func):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()


# 布置界面
window = Tk()
window.title("Zack的下载器")
window.geometry("600x265+490+250")
window.config(bg="#FAFAFA")
# 设置窗口是否可以变化长宽,默认可变
window.resizable(width=False, height=False)
 
lable1_1 = Label(window, text='下载文件: ', font=('微软雅黑', 20), fg='blue', bg="#FAFAFA")
lable1_1.place(x=20, y=20)
 
lable1_2 = Label(window, text="安装目录:", font=('微软雅黑', 20), fg='blue', bg="#FAFAFA")
lable1_2.place(x=20, y=72)
 
# 进度条的实现
lable1_3 = Label(text="下载进度:", font=('微软雅黑', 20), bg="#FAFAFA", fg="blue")
lable1_3.place(x=20, y=122)
canvas = Canvas(window, width=420, height=25, bg="#FFF0F5")
canvas.place(x=150, y=130)
 
entry_1 = Entry(window, font=('微软雅黑', 18), width=30, bg='white')
entry_1.place(x=150, y=30)
 
entry_2 = Entry(window, font=('微软雅黑', 18), width=30, bg='white')
entry_2.place(x=150, y=80)
 
button_1 = Button(window, text="下载", font=("微软雅黑", 20), bg='Snow', activeforeground='gold', activebackground='green',
                  fg="black", command=lambda: thread_it(get_zhu))
button_1.place(x=20, y=200, width=120)
 
button_2 = Button(window, text="退出", font=("微软雅黑", 20), bg='Snow', activeforeground='gold', activebackground='green',
                  fg="black", command=window.quit)
button_2.place(x=450, y=200, width=120)
 
button_3 = Button(window, text="...", font=("微软雅黑", 15), bg='Snow', activeforeground='gold', activebackground='green',
                  fg="black", command=get_wen)
button_3.place(x=535, y=80, width=40)
 
button_4 = Button(window, text="复制", font=("微软雅黑", 20), bg='Snow', activeforeground='gold', activebackground='green',
                  fg="black", command= get_copy)
button_4.place(x=165, y=200, width=120)
 
button_5 = Button(window, text="粘贴", font=("微软雅黑", 20), bg='Snow', activeforeground='gold', activebackground='green',
                  fg="black", command= get_paste)
button_5.place(x=310, y=200, width=120)
 
window.mainloop()