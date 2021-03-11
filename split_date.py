# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2021-03-11 16:10:17
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2021-03-11 16:12:45


from datetime import datetime, timedelta
import calendar


def get_date_range(start_date, end_date):
    date_range = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    middle_date = start_date
    while middle_date <= end_date:
        _, monthlen = calendar.monthrange(middle_date.year, middle_date.month)
        middle_month_max = middle_date.replace(day=monthlen)
        middle_month_max = middle_month_max if end_date > middle_month_max else end_date
        sdate = datetime.strftime(middle_date, '%Y-%m-%d')
        edate = datetime.strftime(middle_month_max, '%Y-%m-%d')
        date_range.append([sdate, edate])
        middle_date = middle_month_max + timedelta(days=1)

    return date_range
