# @Author: chunyang.xu
# @Date:   2021-06-29 07:30:04
# @Last Modified by:   longf
# @Last Modified time: 2021-06-29 08:31:04

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as pg
import time
import random

py = 272
px1 = [669, 875, 689]
px2 = [1070, 1274, 1466]

back = (89, 92)
first = (251, 799)
delp1 = (1889, 103)
delp2 = (931, 574)


while True:
    time.sleep(0.5)
    pg.click(first[0], first[1])
    time.sleep(0.5)
    x1 = random.sample(px1, 1)
    x = x1 + px2
    for i in x:
        pg.click(i, py)
    pg.click(delp1[0], delp1[1])
    pg.click(delp2[0], delp2[1])
    time.sleep(0.5)
    pg.click(back[0], back[1])

