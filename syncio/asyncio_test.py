'''
@Author: longfengpili
@Date: 2020-03-09 09:45:10
@LastEditTime: 2020-03-09 19:56:14
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import threading
from queue import Queue
import time
 
queue = Queue()
 
 
def put_data_in_queue():
    for i in range(10):
        queue.put(i)
 
 
class MyThread(threading.Thread):
    def run(self):
        while not queue.empty():
            sleep_times = queue.get()
            print(sleep_times)
            time.sleep(sleep_times)
            queue.task_done()
 
 
def main_function():
    threads_num = 6
    while True:
        put_data_in_queue()
        for i in range(threads_num):
            myThread = MyThread()
            myThread.setDaemon(True)
            myThread.start()
        queue.join()
        time.sleep(3)

main_function()