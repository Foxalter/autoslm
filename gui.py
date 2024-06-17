import datetime
import threading
from time import sleep
from tkinter import *
from tkinter.ttk import *
import main as m

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_text_lb4no8xs = self.__tk_text_lb4no8xs()
        self.tk_button_start = self.__tk_button_start()
        self.tk_entry_adb = self.__tk_entry_adb()
        self.tk_button_stop = self.__tk_button_stop()
        self.icon = 'template\shortcut.ico'

    def __win(self):
        self.title("自动史莱姆")
        # 设置窗口大小、居中
        width = 621
        height = 271
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        

    def __tk_text_lb4no8xs(self):
        text = Text(self)
        text.place(x=10, y=120, width=601, height=143)
        return text

    def __tk_button_start(self):
        btn = Button(self, text="开始")
        btn.place(x=20, y=30, width=90, height=40)
        return btn
    
    def __tk_entry_adb(self):
        ety = Entry(self, text="输入你的adb")
        ety.place(x=150, y=30, width=200, height=40)
        return ety

    def __tk_button_stop(self):
        btn = Button(self, text="停止")
        btn.place(x=440, y=30, width=90, height=40)
        return btn


class Win(WinGUI):
    flag = False

    def __init__(self):
        super().__init__()
        self.__event_bind()

    def __event_bind(self):
        self.tk_button_start.config(command=self.start)
        self.tk_button_stop.config(command=self.stop)
        self.iconbitmap(self.icon)

    def start(self):
        self.flag = True
        self.adb_url = self.tk_entry_adb.get()
        
        threading.Thread(target=self.print_info).start()

    def stop(self):
        self.flag = False

    def print_info(self):
        info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tk_text_lb4no8xs.insert(1.0, info + ": " + self.adb_url + "\r\n")
        d = m.init(adb_url=self.adb_url)
        while self.flag:
            info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = m.screen(d)
            to_msg = ""
            if msg['to_element'] =='fire':
                to_msg = r"  去火！"
            if msg['to_element'] =='wooden':
                to_msg = r"  去木！"
            if msg['to_element'] =='water':
                to_msg = r"  去水！"
            self.tk_text_lb4no8xs.insert(1.0, info + to_msg + "\r\n")
            # sleep(1)


if __name__ == "__main__":

    win = Win()
    win.mainloop()