# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2020-06-24 10:01:17
# @Last Modified time: 2020-06-24 10:03:33
# @github: https://github.com/longfengpili

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from datetime import datetime, timedelta
import calendar

def get_month_begin_end(month:str, st:str, et:str, interval=3):
    result = re.match('\d{4}-\d{2}$', month)
    if result:
        dateparse = datetime.strptime(month, '%Y-%m')
        year, month, day = dateparse.year, dateparse.month, dateparse.day
        monthlen = calendar.monthlen(year, month)
    else:
        raise ValueError(f"【{date}】 Error,  Should ['%Y-%m'] format !")
    
    st_cal = dateparse - timedelta(interval)
    st_cal = datetime.strftime(st_cal, '%Y-%m-%d')
    st_date = max(st, st_cal)
    et_cal = dateparse + timedelta(monthlen + interval - 1)
    et_cal = datetime.strftime(et_cal, '%Y-%m-%d')
    et_date = min(et, et_cal)
    return st_date, et_date
    
def get_months(st:str, et:str, interval=3):
    st_time = datetime.strptime(st, '%Y-%m-%d')
    st_year, st_month, st_day = st_time.year, st_time.month, st_time.day
    et_time = datetime.strptime(et, '%Y-%m-%d')
    et_year, et_month, et_day = et_time.year, et_time.month, et_time.day
    et_monthlen = calendar.monthlen(et_year, et_month)
    
    months = (et_year - st_year) * 12 + et_month
    months_all = [f'{st_year + i // 12}-{i % 12 + 1:0>2d}' for i in range(st_month-1, months)]
    
    if st_day <= interval:
        begin = f"{st_year + (st_month - 2)// 12}-{(st_month - 2) % 12 + 1:0>2d}"
        months_all.insert(0, begin)
    if et_monthlen - et_day < interval:
        end = f"{et_year + et_month // 12}-{et_month % 12 + 1:0>2d}"
        months_all.append(end)
        
    return months_all

def split_date(st:str, et:str, interval=3):
    months_dict = {}
    months_all = get_months(st, et, interval)
    for month in months_all:
        result = get_month_begin_end(month, st, et, interval=interval)
        months_dict[month] = result
    
    return months_dict


if __name__ == '__main__':
    st = '2020-12-04'
    et = '2022-11-30'
    months = split_date(st, et, interval=3)
    print(months)
