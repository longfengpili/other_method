import win32gui
import win32con
import win32clipboard as w
import time

def get_text():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    print(d)
    return d

def set_text(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def send_message_touser(user, content):
    set_text(content)
    qqhd = win32gui.FindWindow(None, user)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qqhd, 258, 22, 2080193)
    win32gui.SendMessage(qqhd, 770, 0, 0)
    # 模拟按下回车键
    win32gui.SendMessage(qqhd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qqhd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def sent_message_tousers(users, content):
    for user in users:
        send_message_touser(user, content)
        time.sleep(3)

