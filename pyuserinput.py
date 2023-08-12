# @Author: chunyang.xu
# @Date:   2021-06-29 07:30:04
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-04-06 08:16:30

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui as pg
import time
# import random

click1 = [1416, 316]
click2 = [810, 591]
click3 = [1112, 650]
click4 = [1052, 609]
click5 = [1258, 568]
click6 = [841, 558]
click7 = [1151, 646]
click8 = [1114, 601]

clicks = [click1, click2, click3, click4, click5, click6, click7, click8]

while True:
    for click in clicks:
        time.sleep(1)
        pg.click(click[0], click[1])

    break

