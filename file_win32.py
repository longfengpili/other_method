'''
@Author: longfengpili
@Date: 2019-11-15 10:12:11
@LastEditTime: 2019-11-15 12:42:08
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from win32.lib import win32con
import time
import os
import win32gui
import win32api

class File(object):
    
    def __init__(self, filepath):
        self.filepath = filepath.replace('/', '\\') #需要改成windows支持的格式
        self.filename = self.filepath.split('\\')[-1]

    def open_file(self):
        os.system(f'explorer {self.filepath}')

    def get_file_hwnd(self):
        clsname = None
        title = None
        hwndlist = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwndlist)
        for hwnd in hwndlist:
            clsname = win32gui.GetClassName(hwnd)  # 类名
            title = win32gui.GetWindowText(hwnd)    #文件名
            if self.filename in title:
                break
            else:
                hwnd = None
        return hwnd, clsname, title

    def close_file(self):
        hwnd, clsname, title = self.get_file_hwnd()
        if win32gui.IsWindowVisible(hwnd):
            print(hwnd, clsname, title)
            #保存退出
            # win32gui.SetForegroundWindow(hwnd) #激活窗口
            # time.sleep(1)
            # win32api.keybd_event(17, 0, 0, 0)
            # win32api.keybd_event(83, 0, 0, 0)
            # win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
            # win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)  # 关闭窗口

    def del_file(self):
        try:
            os.system(f'del {self.filepath}')
        except Exception as e:
            print(e)
