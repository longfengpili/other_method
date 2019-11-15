# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2019-11-15 17:41:38
# @Last Modified time: 2019-11-15 19:04:53
# @github: https://github.com/longfengpili

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from queue import Queue
import threading
from threading import Thread
import time
import random
from datetime import datetime

# 创建队列实例， 用于存储任务
queue = Queue()

# 定义需要线程池执行的任务


def do_job():
	while True:
	    st = time.time()
	    # i = queue.get()
	    time.sleep(random.randint(1, 10))
	    et = time.time()
	    et_str = datetime.utcfromtimestamp(et)
	    print(f'【{et_str}】【time】{round(et-st, 2)}, curent: {threading.current_thread()}')
	    queue.task_done()


if __name__ == '__main__':
    # 创建包括2个线程的线程池
    for i in range(4):
        t = Thread(target=do_job)
        t.daemon = True  # 设置线程daemon  主线程退出，daemon线程也会推出，即时正在运行
        t.start()

    # 塞进10个任务到队列
    for i in range(20):
        queue.put(i)

    queue.join()