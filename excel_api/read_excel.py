'''
@Author: longfengpili
@Date: 2019-11-11 14:57:05
@LastEditTime: 2019-12-11 20:05:41
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import xlrd
import sys

import logging
from logging import config
config.fileConfig('tutoriallog.conf')
excel_logger = logging.getLogger('excel')


class ReadDataFromExcel(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def open_excel(self):
        try:
            book = xlrd.open_workbook(self.filepath)
            return book
        except Exception as e:
            excel_logger.error(e)
            sys.exit(0)

    def get_sheets(self):
        book = self.open_excel()
        sheets = book.sheets()
        sheets = dict([(sheet.name, sheet) for sheet in sheets])
        return sheets

    def open_sheet(self, sheetname):
        book = self.open_excel()
        sheet = book.sheet_by_name(sheetname)
        return sheet

    def get_sheet_values(self, sheetname):
        sheet = self.open_sheet(sheetname)
        sheet_values = [sheet.row_values(row) for row in range(sheet.nrows)]
        return sheet_values

    def get_sheet_values_by_columns(self, sheetname, select_columns, header_row=0):
        '''
        @description: 根据列名选择
        @param {type} 
        【sheetname {str}】：表格名
        【select_columns {list}】：要选择的列名
        【header_row {int}】：header所在的row
        @return: 
        '''
        sheet_values = []
        sheet = self.open_sheet(sheetname)
        headers = sheet.row_values(header_row)
        select_columns_index = [headers.index(column) for column in select_columns]
        sheet_values = [sheet.col_values(column)[header_row:] for column in select_columns_index]
        sheet_values = list(zip(*sheet_values))
        return sheet_values

        
