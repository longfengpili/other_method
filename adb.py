#!/usr/bin/env python
# coding=UTF-8
'''
@Author: longfengpili
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
@Date: 2019-05-06 16:12:41
@LastEditTime: 2019-05-06 16:52:31
'''
import os,sys
import random
from datetime import datetime,date
import time

import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



class adbapi():
    def __init__(self):
        self.phonedir = 'aniland'
        self.temppath = '../../temp/'

    def restart_adb(self,stime):
        time.sleep(stime)
        os.system('adb start-server')
        logging.info('restart adb!')

    def __screen_position(self,box):
        try:
            x1,y1,x2,y2 = box
        except:
            x1,y1,x2,y2 = [i for t in box for i in t]
        x = random.randint(x1+int((x2-x1)/4),x2-int((x2-x1)/4))
        y = random.randint(y1+int((y2-y1)/4),y2-int((y2-y1)/4))
        return x,y

    def tap_screen(self,box,double_click=False):
        x,y = self.__screen_position(box)
        if double_click:
            os.system('adb shell input tap {} {}'.format(x, y))
            time.sleep((random.random()+1) * 0.5)
            os.system('adb shell input tap {} {}'.format(x, y))
        os.system('adb shell input tap {} {}'.format(x, y))
        # logging.info(f'tap {x} {y}')

    def swipe_screen(self):
        x = random.randint(600,1500)
        y = random.randint(720,750)
        swipe = random.randint(100,150)
        os.system(f"adb shell input swipe {x} {y} {x} {y - swipe}")
        # logging.info(f"swipe {x} {y} {x} {y - swipe}")

    def mkdir_for_screenshot(self):
        dir_p = os.popen(f"adb shell ls /mnt/sdcard/ |findstr {self.phonedir}").read()
        
        if not dir_p:
            os.system(f'adb shell mkdir /mnt/sdcard/{self.phonedir}/')
            logging.info(f'adb shell mkdir /mnt/sdcard/{self.phonedir}/')

    def pull_screenshot(self,dirpath=None,filename=None,interval=0):
        '''
        (1,1.5)*interval
        '''
        time.sleep((random.random()/2 + 1) * interval)
        self.mkdir_for_screenshot()
        if not dirpath:
            dirpath = self.temppath

        if not filename:
            filename = datetime.now().strftime('%Y_%m_%d_%H%M%S')
        os.system(f'adb shell screencap -p /mnt/sdcard/{self.phonedir}/{filename}.png')
        os.system(f'adb pull /mnt/sdcard/{self.phonedir}/{filename}.png {dirpath} 1>nul')
        os.system(f'adb shell rm /mnt/sdcard/{self.phonedir}/{filename}.png 1>nul') 
        picpath = f'{dirpath}{filename}.png'
        return picpath


if __name__ == "__main__":
    adbapi = adbapi()
    filename = sys.argv[1]
    adbapi.pull_screenshot(filename=filename)
    
