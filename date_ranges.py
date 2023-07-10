# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2022-09-09 11:21:43
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-06-26 11:43:00


import logging
import calendar
from datetime import datetime, timedelta
dlogger = logging.getLogger(__name__)


class DateFuncNew:

    def __init__(self, unit: str):
        self.unit = unit

    def parse_dates(self, *dates, parsetype: str = 'strptime', formatter: str = '%Y-%m-%d'):
        if parsetype == 'strptime':
            dates = [datetime.strptime(date, formatter) for date in dates]
        else:
            dates = [datetime.strftime(date, formatter) for date in dates]

        return dates

    def update_date(self, start_date: str, end_date: str, updatetype='maxdays', maxdays: int = 0, 
                    begin_date: str = '1987-01-05', ismfirst: str = False):
        if begin_date > end_date:
            raise ValueError(f"begin_date({begin_date}) max than end_date({end_date})")

        update_start_date, update_end_date, update_begin_date = self.parse_dates(start_date, end_date, begin_date)
        today = datetime.today()
        if updatetype == 'maxdays' and maxdays:
            _update_start_date = update_end_date - timedelta(days=maxdays)
            update_start_date = max(update_start_date, _update_start_date)

        update_start_date = update_start_date.replace(day=1) if ismfirst else update_start_date
        if self.unit == 'day':
            pass
        elif self.unit == 'week':
            s_weekday, e_weekday = update_start_date.weekday(), update_end_date.weekday()
            update_start_date -= timedelta(days=s_weekday)
            update_end_date += timedelta(days=(6 - e_weekday))
        elif self.unit == 'month':
            _, monthlen = calendar.monthrange(update_end_date.year, update_end_date.month)
            update_end_date = update_end_date.replace(day=monthlen)
        else:
            raise ValueError(f"Not support unit {self.unit} !!!")

        update_start_date = max(update_start_date, update_begin_date)
        update_end_date = min(update_end_date, today)
        update_start_date, update_end_date = self.parse_dates(update_start_date, update_end_date, parsetype='strftime')
        # changeinfo = f" start_date({start_date}) change to {update_start_date}, end_date({end_date}) change to {update_end_date}"
        # dlogger.warning(f"Unit: {self.unit}(begin date: {begin_date}), {changeinfo} !!!")
        return update_start_date, update_end_date

    def get_date_ranges(self, start_date: str, end_date: str, days: int = 0):
        date_ranges = []
        start_date, end_date = self.parse_dates(start_date, end_date)
        _start_date = start_date
        while _start_date <= end_date:
            if self.unit == 'day':
                _end_date = _start_date + timedelta(days=days)
            elif self.unit == 'week':
                _end_date = _start_date + timedelta(days=days)
                s_weekday = _end_date.weekday()
                _end_date += timedelta(days=6 - s_weekday)
            elif self.unit == 'month':
                _end_date = _start_date + timedelta(days=days)
                _, monthlen = calendar.monthrange(_end_date.year, _end_date.month)
                _end_date = _end_date.replace(day=monthlen)
            else:
                raise ValueError(f"Not support unit {self.unit} !!!")

            _end_date = min(_end_date, end_date)
            dates = self.parse_dates(_start_date, _end_date, parsetype='strftime')
            date_ranges.append(dates)
            _start_date = _end_date + timedelta(days=1)

        # start_date, end_date = self.parse_dates(start_date, end_date, parsetype='strftime')
        # dlogger.info(f"unit: {self.unit}, ({start_date}, {end_date}), date_range: {date_ranges} !!!")
        return date_ranges

    def get_start_and_end_dates(self, start_date: str, end_date: str, days: int = 0):
        date_ranges = self.get_date_ranges(start_date, end_date, days=days)
        start_days, end_days = [date[0] for date in date_ranges], [date[1] for date in date_ranges]
        # dlogger.info(f"unit: {self.unit}, start_days ({start_days}), end_days: {end_days} !!!")
        return start_days, end_days
